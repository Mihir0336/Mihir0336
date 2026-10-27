"""Activity card: contribution calendar, streaks and languages, fetched live from GitHub."""

import datetime as dt
import json
import os
import re
import urllib.request

from cards import LANG_COLOR
from content import USER
from kit import Svg, measure

UA = {"User-Agent": f"{USER}-profile-cards"}


def _get(url, api=False):
    headers = dict(UA)
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if api and token:
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
        return r.read().decode()


def calendar():
    """[(date, count, level)] for the last year, from the public contributions page (includes private work if the
    owner has "private contributions" switched on in their profile settings)."""
    html = _get(f"https://github.com/users/{USER}/contributions")
    cells = re.findall(r'data-date="(\d{4}-\d\d-\d\d)" id="(contribution-day-component-\d+-\d+)" data-level="(\d)"', html)
    counts = {}
    for cid, tip in re.findall(r'for="(contribution-day-component-\d+-\d+)"[^>]*>([^<]*)', html):
        m = re.match(r"\s*(\d+|No) contributions?", tip)
        counts[cid] = 0 if not m or m.group(1) == "No" else int(m.group(1))
    # GitHub's own 0-4 shading level rides along so the card matches the profile graph
    days = sorted((dt.date.fromisoformat(d), counts.get(cid, 0), int(lv)) for d, cid, lv in cells)
    if len(days) < 300:
        raise RuntimeError(f"calendar looks wrong: {len(days)} days")
    return days


def languages():
    repos = json.loads(_get(f"https://api.github.com/users/{USER}/repos?per_page=100", api=True))
    total = {}
    for r in repos:
        if r["fork"] or r["name"] == USER:
            continue
        for lang, n in json.loads(_get(r["languages_url"], api=True)).items():
            total[lang] = total.get(lang, 0) + n
    return sorted(total.items(), key=lambda kv: -kv[1])


def streaks(days):
    longest = run = 0
    best = (None, None)
    start = None
    for d, n, _ in days:
        if n:
            if run == 0:
                start = d
            run += 1
            if run > longest:
                longest, best = run, (start, d)
        else:
            run = 0
    # current streak: today may still be empty, so count back from the last day with work if it is today or yesterday
    cur = 0
    seq = list(reversed(days))
    if seq and seq[0][1] == 0:
        seq = seq[1:]
    for _, n, _ in seq:
        if not n:
            break
        cur += 1
    return cur, longest, best


def fmt_day(d):
    return f"{d.day} {d.strftime('%b')}"


def lang_col(lang, theme, fallback):
    col = LANG_COLOR.get(lang)
    extra = {"CSS": "#663399", "HTML": "#e34c26", "Hack": "#878787", "Blade": "#f7523f", "SCSS": "#c6538c", "Shell": "#89e051"}
    col = col or extra.get(lang) or fallback
    if theme == "dark" and lang == "Lua":
        col = "#7c83ff"
    if theme == "dark" and lang == "CSS":
        col = "#9b6fd6"
    return col


def card(theme, days, langs, mobile=False):
    total = sum(n for _, n, _ in days)
    cur, longest, (ls, le) = streaks(days)
    busiest = max(days, key=lambda x: x[1])
    today = days[-1][0]
    title = (
        f"{total:,} contributions in the last 12 months. Current streak {cur} days, longest {longest} days."
    )
    stats = [
        (f"{total:,}", "contributions", "last 12 months"),
        (str(cur), "day streak now", "and counting" if cur else "starts today"),
        (str(longest), "day longest streak", f"{fmt_day(ls)} to {fmt_day(le)}" if ls else "—"),
        (str(busiest[1]), "on the busiest day", fmt_day(busiest[0]) + f" {busiest[0].year}"),
    ]

    # pad the calendar to whole weeks starting on Sunday
    first = days[0][0]
    pad = (first.weekday() + 1) % 7
    weeks = []
    col = [None] * pad
    for d, n, lv in days:
        col.append((d, n, lv))
        if len(col) == 7:
            weeks.append(col)
            col = []
    if col:
        weeks.append(col + [None] * (7 - len(col)))
    if mobile:
        weeks = weeks[-26:]
    top = [(l, n) for l, n in langs[:6]]
    rest = sum(n for _, n in langs[6:])
    if rest:
        top.append(("Other", rest))
    lsum = sum(n for _, n in top) or 1

    if not mobile:
        w, h = 1200, 520
        cell, gap = 16, 4
        hx, hy = (w - len(weeks) * (cell + gap) + gap) / 2 + 14, 222
        s = Svg(w, h, title, theme)
        c = s.c
        s.frame(rx=20, glow=(0, 0, 520))
        for i, (big, lab, sub) in enumerate(stats):
            x = 40 + i * 284
            if i:
                s.add(f'<line x1="{x - 24}" y1="40" x2="{x - 24}" y2="128" stroke="{c["line2"]}"/>')
            s.text(x, 86, big, "sans-sb", 46, c["accent"] if i == 0 else c["fg"], tracking=-0.03)
            s.text(x, 112, lab, "sans", 15, c["muted"])
            s.text(x, 132, sub, "mono", 12, c["subtle"])
        s.add(f'<line x1="24" y1="166" x2="{w - 24}" y2="166" stroke="{c["line"]}"/>')
        lab_size = 11
        legend_y = hy + 7 * (cell + gap) + 22
    else:
        w = 600
        cell, gap = 15, 4
        hx, hy = (w - len(weeks) * (cell + gap) + gap) / 2 + 14, 330
        h = 0
        s = None

    if mobile:
        rows_l = -(-len(top) // 2)
        h = hy + 7 * (cell + gap) + 60 + 70 + rows_l * 34 + 30
        s = Svg(w, h, title, theme)
        c = s.c
        s.frame(rx=20, glow=(0, 0, 400))
        for i, (big, lab, sub) in enumerate(stats):
            x = 30 + (i % 2) * 280
            y = 40 + (i // 2) * 126
            s.text(x, y + 46, big, "sans-sb", 44, c["accent"] if i == 0 else c["fg"], tracking=-0.03)
            s.text(x, y + 74, lab, "sans", 17, c["muted"])
            s.text(x, y + 96, sub, "mono", 14, c["subtle"])
        s.add(f'<line x1="24" y1="{hy - 52}" x2="{w - 24}" y2="{hy - 52}" stroke="{c["line"]}"/>')
        lab_size = 13
        legend_y = hy + 7 * (cell + gap) + 24

    # heatmap
    s.css.append("@keyframes hm{from{opacity:0}to{opacity:1}}.hm{animation:hm .5s ease-out both}")
    shades = [c["heat0"]] + [c["accent"]] * 4
    alpha = [1, 0.32, 0.55, 0.78, 1]
    last_month = None
    for wi, wk in enumerate(weeks):
        x = hx + wi * (cell + gap)
        first_day = next((d for d in wk if d), None)
        if first_day and first_day[0].month != last_month and first_day[0].day <= 7:
            if wi < len(weeks) - 2:
                s.text(x, hy - 12, first_day[0].strftime("%b"), "mono", lab_size, c["subtle"])
            last_month = first_day[0].month
        elif first_day and last_month is None:
            last_month = first_day[0].month
        cells = []
        for di, d in enumerate(wk):
            if not d:
                continue
            lv = d[2]
            cells.append(
                f'<rect x="{x}" y="{hy + di * (cell + gap)}" width="{cell}" height="{cell}" rx="4" fill="{shades[lv]}"'
                + (f' fill-opacity="{alpha[lv]}"' if lv else "")
                + "/>"
            )
        s.add(f'<g class="hm" style="animation-delay:{wi * 0.018:.3f}s">{"".join(cells)}</g>')
    for di, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        s.text(hx - 12, hy + di * (cell + gap) + cell - 4, name, "mono", lab_size, c["subtle"], anchor="end")

    # less/more legend + as-of
    gx = hx + len(weeks) * (cell + gap) - gap
    lx = gx - measure("more", "mono", lab_size) - 8 - 5 * 16 + 4
    s.text(lx - 10, legend_y + 10, "less", "mono", lab_size, c["subtle"], anchor="end")
    for i in range(5):
        s.add(
            f'<rect x="{lx + i * 16}" y="{legend_y}" width="12" height="12" rx="3" fill="{shades[i]}"'
            + (f' fill-opacity="{alpha[i]}"' if i else "")
            + "/>"
        )
    s.text(lx + 5 * 16 + 6, legend_y + 10, "more", "mono", lab_size, c["subtle"])
    s.text(hx, legend_y + 10, f"as of {fmt_day(today)} {today.year}", "mono", lab_size, c["subtle"])

    # languages
    ly = legend_y + 56
    s.text(hx if not mobile else 30, ly, "Languages across public repos", "sans-m", 15 if not mobile else 18, c["fg"])
    bx = hx if not mobile else 30
    bw = (gx - hx) if not mobile else w - 60
    by = ly + 18
    s.defs.append(f'<clipPath id="lb"><rect x="{bx}" y="{by}" width="{bw}" height="10" rx="5"/></clipPath>')
    parts, x = [], bx
    for lang, n in top:
        seg = bw * n / lsum
        parts.append(f'<rect x="{x:.1f}" y="{by}" width="{max(seg - 2, 0):.1f}" height="10" fill="{lang_col(lang, s.theme, c["subtle"])}"/>')
        x += seg
    s.add(f'<g clip-path="url(#lb)">{"".join(parts)}</g>')
    if not mobile:
        x = bx
        for lang, n in top:
            label = f"{lang} {n / lsum * 100:.1f}%"
            s.add(f'<circle cx="{x + 5}" cy="{by + 34}" r="5" fill="{lang_col(lang, s.theme, c["subtle"])}"/>')
            s.text(x + 16, by + 38.5, label, "mono", 12.5, c["muted"])
            x += 16 + measure(label, "mono", 12.5) + 28
    else:
        for i, (lang, n) in enumerate(top):
            x = 30 + (i % 2) * 280
            y = by + 40 + (i // 2) * 34
            s.add(f'<circle cx="{x + 6}" cy="{y - 5}" r="6" fill="{lang_col(lang, s.theme, c["subtle"])}"/>')
            s.text(x + 20, y, f"{lang} {n / lsum * 100:.1f}%", "mono", 15, c["muted"])
    s.save("activity.m" if mobile else "activity")


def build_all():
    days = calendar()
    langs = languages()
    for theme in ("dark", "light"):
        for m in (False, True):
            card(theme, days, langs, m)
    return days, langs
