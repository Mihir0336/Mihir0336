"""Shared building blocks: themes, embedded fonts, text measurement and the Svg writer.

Every card is a standalone SVG rendered inside <img>, so it cannot load web fonts.
Each file embeds only the glyphs it actually uses, subset to WOFF2.
"""

import base64
import io
import logging
import re
from functools import lru_cache
from pathlib import Path

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

logging.getLogger("fontTools").setLevel(logging.ERROR)

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "scripts" / "fonts"
ICON_DIR = ROOT / "scripts" / "icons"
ASSETS = ROOT / "assets"

THEMES = {
    "dark": {
        "bg": "#0b0b0c",
        "card": "#111113",
        "card2": "#17171a",
        "line": "#232327",
        "line2": "#323238",
        "fg": "#ededef",
        "muted": "#b1b1b8",
        "subtle": "#8e8e96",
        "accent": "#ffb020",
        "accent_fg": "#1a1200",
        "green": "#4ade80",
        "heat0": "#1c1c20",
        "glow": 0.22,
    },
    "light": {
        "bg": "#fafaf9",
        "card": "#ffffff",
        "card2": "#f5f5f4",
        "line": "#e7e5e4",
        "line2": "#d6d3d1",
        "fg": "#0b0b0c",
        "muted": "#52525b",
        "subtle": "#6b6b73",
        "accent": "#b45309",
        "accent_fg": "#fffbeb",
        "green": "#16a34a",
        "heat0": "#efedea",
        "glow": 0.14,
    },
}

# key -> (file, css family name)
FONTS = {
    "sans": ("Geist-Regular.ttf", "G4"),
    "sans-m": ("Geist-Medium.ttf", "G5"),
    "sans-sb": ("Geist-SemiBold.ttf", "G6"),
    "mono": ("GeistMono-Regular.ttf", "M4"),
    "mono-m": ("GeistMono-Medium.ttf", "M5"),
    "serif": ("InstrumentSerif-Italic.ttf", "S4"),
}


@lru_cache(maxsize=None)
def _font(key):
    return TTFont(FONT_DIR / FONTS[key][0])


@lru_cache(maxsize=None)
def _metrics(key):
    f = _font(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upm = f["head"].unitsPerEm
    return cmap, hmtx, upm


def measure(text, key, size, tracking=0.0):
    cmap, hmtx, upm = _metrics(key)
    units = 0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            raise ValueError(f"{FONTS[key][0]} has no glyph for {ch!r}")
        units += hmtx[g][0]
    return units * size / upm + tracking * size * max(len(text) - 1, 0)


def wrap(text, key, size, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and measure(trial, key, size) > width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


@lru_cache(maxsize=None)
def _subset_b64(key, chars):
    # recalcTimestamp=False keeps the output byte-identical between runs, so the
    # refresh workflow only commits when the data actually changed
    f = TTFont(FONT_DIR / FONTS[key][0], recalcTimestamp=False)
    opts = Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []
    opts.notdef_outline = False
    sub = Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


@lru_cache(maxsize=None)
def icon_path(slug):
    """Path data of a 24x24 Simple Icons glyph."""
    svg = (ICON_DIR / f"{slug}.svg").read_text(encoding="utf-8")
    return re.search(r'<path d="([^"]+)"', svg).group(1)


class Svg:
    def __init__(self, w, h, title, theme):
        self.w, self.h = w, h
        self.title = title
        self.c = THEMES[theme]
        self.theme = theme
        self.parts = []
        self.defs = []
        self.css = []
        self.used = {}
        self._ids = 0

    def uid(self, prefix="u"):
        self._ids += 1
        return f"{prefix}{self._ids}"

    def add(self, s):
        self.parts.append(s)
        return self

    def text(self, x, y, s, key="sans", size=14, fill=None, anchor="start", tracking=0.0, extra=""):
        self.used.setdefault(key, set()).update(s)
        fam = FONTS[key][1]
        ls = f' letter-spacing="{tracking * size:.2f}"' if tracking else ""
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        self.parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}"'
            f' fill="{fill or self.c["fg"]}"{a}{ls}{extra}>{esc(s)}</text>'
        )
        return self

    def runs(self, x, y, runs, size, anchor="start"):
        """One line made of (text, font key, colour) runs, e.g. a sans phrase with a serif accent word."""
        spans = []
        for run in runs:
            s, key, fill = run[:3]
            fs = f' font-size="{run[3]}"' if len(run) > 3 else ""
            self.used.setdefault(key, set()).update(s)
            spans.append(f'<tspan font-family="{FONTS[key][1]}" fill="{fill}"{fs}>{esc(s)}</tspan>')
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        self.parts.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}"{a} xml:space="preserve">{"".join(spans)}</text>')
        return self

    def icon(self, slug, x, y, size, fill):
        s = size / 24
        self.parts.append(f'<path transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" d="{icon_path(slug)}" fill="{fill}"/>')
        return self

    def frame(self, rx=18, fill=None, glow=None):
        """Card background with a hairline border; glow=(cx, cy, r) adds a soft accent light."""
        c = self.c
        self.add(f'<rect x="0.5" y="0.5" width="{self.w - 1}" height="{self.h - 1}" rx="{rx}" fill="{fill or c["card"]}" stroke="{c["line"]}"/>')
        if glow:
            gid = self.uid("g")
            cx, cy, r = glow
            self.defs.append(
                f'<radialGradient id="{gid}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'
                f'<stop offset="0" stop-color="{c["accent"]}" stop-opacity="{c["glow"]}"/>'
                f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></radialGradient>'
            )
            self.add(f'<rect x="0.5" y="0.5" width="{self.w - 1}" height="{self.h - 1}" rx="{rx}" fill="url(#{gid})"/>')
        return self

    def pill(self, x, y, label, key="mono", size=12, fill=None, color=None, stroke=None, padx=10, h=24):
        c = self.c
        w = measure(label, key, size) + padx * 2
        self.add(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{fill or c["card2"]}"'
            + (f' stroke="{stroke}"' if stroke else "")
            + "/>"
        )
        self.text(x + padx, y + h / 2 + size * 0.35, label, key, size, color or c["muted"])
        return w

    def render(self):
        faces = []
        for key, chars in sorted(self.used.items()):
            data = _subset_b64(key, "".join(sorted(chars)))
            faces.append(f'@font-face{{font-family:"{FONTS[key][1]}";src:url(data:font/woff2;base64,{data}) format("woff2")}}')
        css = "".join(faces) + "".join(self.css) + "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        t = esc(self.title)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}"'
            f' role="img" aria-label="{t}"><title>{t}</title><style>{css}</style>'
            f'<defs>{"".join(self.defs)}</defs>{"".join(self.parts)}</svg>'
        )

    def save(self, name):
        out = ASSETS / self.theme / f"{name}.svg"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(self.render(), encoding="utf-8")
        return out


def both(fn, *args, **kw):
    """Run a card builder for both themes."""
    for theme in THEMES:
        fn(theme, *args, **kw)
