"""Static cards: hero, link chips, section headers, experience, projects, stack, footer."""

from content import EDUCATION, EXPERIENCE, PROFILE, PROJECTS, SHOW_WORK, STACK, USER
from kit import Svg, measure, wrap

# Brand colours; None means "use the foreground colour" (black logos on a dark card).
BRAND = {
    "javascript": "#F7DF1E", "typescript": "#3178C6", "lua": ("#7c83ff", "#2C2D72"), "php": "#777BB4",
    "html5": "#E34F26", "css3": ("#3b8fd9", "#1572B6"), "react": ("#61DAFB", "#0e9fc0"),
    "nextdotjs": None, "svelte": "#FF3E00", "tailwindcss": "#06B6D4", "shadcnui": None, "framer": "#0055FF",
    "nodedotjs": "#5FA04E", "express": None, "prisma": None, "mysql": "#4479A1", "mongodb": "#47A248",
    "fivem": "#F40552", "git": "#F05032", "github": None, "vercel": None,
    "python": ("#5a9fd4", "#3776AB"), "linux": None, "nginx": "#009639", "pm2": ("#7a8bd9", "#2B037A"),
}


def brand(s, slug):
    v = BRAND.get(slug)
    if v is None:
        return s.c["fg"]
    if isinstance(v, tuple):
        return v[0] if s.theme == "dark" else v[1]
    return v


def dot_grid(s, x, y, w, h, fade_cx, fade_cy, fade_r, step=18):
    """Faint dot grid that fades out away from (fade_cx, fade_cy)."""
    pid, mid, gid = s.uid("p"), s.uid("m"), s.uid("g")
    s.defs.append(
        f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
        f'<circle cx="{step / 2}" cy="{step / 2}" r="1" fill="{s.c["line2"]}"/></pattern>'
        f'<radialGradient id="{gid}" cx="{fade_cx}" cy="{fade_cy}" r="{fade_r}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        f'<mask id="{mid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gid})"/></mask>'
    )
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{pid})" mask="url(#{mid})"/>')


def pulse_dot(s, cx, cy, color, r=4):
    s.css.append("@keyframes pl{0%{r:4px;opacity:.55}80%,100%{r:11px;opacity:0}}.pl{animation:pl 2s ease-out infinite}")
    s.add(f'<circle class="pl" cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')


# ---------------------------------------------------------------- hero

def nui_panel(s, x, y, w, h):
    """A little live diagram of a FiveM NUI round trip: server.lua -> client.lua -> React UI and back."""
    c = s.c
    s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>')
    s.add(f'<line x1="{x}" y1="{y + 40}" x2="{x + w}" y2="{y + 40}" stroke="{c["line"]}"/>')
    for i, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        s.add(f'<circle cx="{x + 20 + i * 16}" cy="{y + 20}" r="5" fill="{col}" opacity=".85"/>')
    s.text(x + 76, y + 24.5, "nui-bridge", "mono", 12, c["subtle"])
    pulse_dot(s, x + w - 64, y + 20, c["green"], 3.5)
    s.text(x + w - 20, y + 24.5, "live", "mono", 12, c["subtle"], anchor="end")

    nodes = [
        ("server.lua", "server side", "lua"),
        ("client.lua", "client side", "lua"),
        ("React · Svelte UI", "NUI frame", "react"),
    ]
    nw, nh = w - 120, 56
    nx = x + 60
    top, bottom = y + 64, y + h - 24 - nh
    gap = (bottom - top) / 2
    ys = [top + i * gap for i in range(3)]
    period = 6.4
    for i, ((title, sub, ic), ny) in enumerate(zip(nodes, ys)):
        s.add(f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="12" fill="{c["card"]}" stroke="{c["line2"]}"/>')
        # brief highlight when a packet lands on this node
        hits = {0: [0.0, 0.94], 1: [0.24, 0.70], 2: [0.47]}[i]
        for t in hits:
            k0 = max(t, 0.001)
            s.add(
                f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="12" fill="none" stroke="{c["accent"]}" stroke-width="1.5" opacity="0">'
                f'<animate attributeName="opacity" dur="{period}s" repeatCount="indefinite" calcMode="linear"'
                f' keyTimes="0;{k0:.3f};{min(t + 0.04, 0.999):.3f};{min(t + 0.12, 0.9995):.3f};1" values="0;0;1;0;0"/></rect>'
            )
        s.add(f'<rect x="{nx + 12}" y="{ny + 11}" width="34" height="34" rx="9" fill="{c["card2"]}"/>')
        s.icon(ic, nx + 19, ny + 18, 20, brand(s, ic))
        s.text(nx + 58, ny + 25, title, "sans-m", 15, c["fg"])
        s.text(nx + 58, ny + 43, sub, "mono", 11.5, c["subtle"])

    down_x, up_x = nx + nw * 0.36, nx + nw * 0.64
    legs = [
        # (x, from y, to y, label, label side, start, end, colour)
        (down_x, ys[0] + nh, ys[1], "TriggerClientEvent", "l", 0.00, 0.22, c["accent"]),
        (down_x, ys[1] + nh, ys[2], "SendNUIMessage", "l", 0.24, 0.46, c["accent"]),
        (up_x, ys[2], ys[1] + nh, "NUI callback", "r", 0.48, 0.68, c["muted"]),
        (up_x, ys[1], ys[0] + nh, "TriggerServerEvent", "r", 0.70, 0.92, c["muted"]),
    ]
    for lx, y0, y1, label, side, t0, t1, col in legs:
        s.add(f'<line x1="{lx}" y1="{y0}" x2="{lx}" y2="{y1}" stroke="{c["line2"]}" stroke-dasharray="3 4"/>')
        arrow = 5 if y1 > y0 else -5
        s.add(f'<path d="M{lx - 4} {y1 - arrow} L{lx} {y1} L{lx + 4} {y1 - arrow}" fill="none" stroke="{c["line2"]}" stroke-width="1.2"/>')
        my = (y0 + y1) / 2 + 4
        if side == "l":
            s.text(lx - 12, my, label, "mono", 11, c["subtle"], anchor="end")
        else:
            s.text(lx + 12, my, label, "mono", 11, c["subtle"])
        a, b = max(t0, 0.001), t1
        s.add(
            f'<circle r="4" fill="{col}" opacity="0">'
            f'<animateMotion dur="{period}s" repeatCount="indefinite" calcMode="linear" path="M{lx} {y0} L{lx} {y1}"'
            f' keyPoints="0;0;1;1" keyTimes="0;{a:.3f};{b:.3f};1"/>'
            f'<animate attributeName="opacity" dur="{period}s" repeatCount="indefinite" calcMode="discrete"'
            f' keyTimes="0;{a:.3f};{b:.3f}" values="0;1;0"/></circle>'
        )


def hero(theme, mobile=False):
    p = PROFILE
    if not mobile:
        s = Svg(1200, 500, f"{p['name']}, {p['role']}. {p['pitch']}", theme)
        c = s.c
        s.frame(rx=22, glow=(1060, 40, 620))
        dot_grid(s, 640, 0, 560, 500, 960, 250, 420)
        sx = 56
        pulse_dot(s, sx + 6, 70, c["green"])
        s.text(sx + 20, 74.5, f"Open to work · {p['location']}", "mono", 13, c["muted"])
        s.text(sx - 3, 168, p["name"], "sans-sb", 80, c["fg"], tracking=-0.035)
        s.runs(sx, 226, [
            ("Real-time web apps ", "sans-m", c["fg"]),
            ("&", "serif", c["accent"], 42),
            (" in-game UIs.", "sans-m", c["fg"]),
        ], 32)
        for i, line in enumerate(wrap(p["pitch"], "sans", 17, 590)):
            s.text(sx, 276 + i * 27, line, "sans", 17, c["muted"])
        rows = [("web", PROFILE["site"].removeprefix("https://")), ("study", EDUCATION)]
        for i, (k, v) in enumerate(rows):
            yy = 410 + i * 28
            s.text(sx, yy, k, "mono", 12.5, c["accent"])
            s.text(sx + 58, yy, v, "mono", 12.5, c["subtle"])
        nui_panel(s, 724, 44, 432, 412)
    else:
        s = Svg(600, 900, f"{p['name']}, {p['role']}. {p['pitch']}", theme)
        c = s.c
        s.frame(rx=22, glow=(560, 20, 420))
        dot_grid(s, 0, 0, 600, 420, 520, 60, 380)
        sx = 36
        pulse_dot(s, sx + 6, 58, c["green"])
        s.text(sx + 20, 63, f"Open to work · {p['location']}", "mono", 15, c["muted"])
        s.text(sx - 2, 148, p["name"], "sans-sb", 66, c["fg"], tracking=-0.035)
        s.runs(sx, 200, [("Real-time web apps ", "sans-m", c["fg"]), ("&", "serif", c["accent"], 40)], 30)
        s.text(sx, 240, "in-game UIs.", "sans-m", 30, c["fg"])
        for i, line in enumerate(wrap(p["pitch"], "sans", 19, 528)):
            s.text(sx, 288 + i * 30, line, "sans", 19, c["muted"])
        nui_panel(s, 36, 440, 528, 420)
    s.save("hero.m" if mobile else "hero")


# ---------------------------------------------------------------- chips

def _glyph(s, kind, x, y, col):
    """16px line glyphs for chips."""
    st = f'fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "mail":
        s.add(f'<rect x="{x}" y="{y + 2}" width="16" height="12" rx="2.5" {st}/><path d="M{x + 1} {y + 3.5} L{x + 8} {y + 9} L{x + 15} {y + 3.5}" {st}/>')
    elif kind == "globe":
        s.add(f'<circle cx="{x + 8}" cy="{y + 8}" r="7" {st}/><ellipse cx="{x + 8}" cy="{y + 8}" rx="3" ry="7" {st}/><path d="M{x + 1} {y + 8} H{x + 15}" {st}/>')
    elif kind == "doc":
        s.add(f'<path d="M{x + 3} {y + 1} H{x + 10} L{x + 14} {y + 5} V{y + 15} H{x + 3} Z" {st}/><path d="M{x + 6} {y + 9} H{x + 11} M{x + 6} {y + 12} H{x + 10}" {st}/>')


def chip(theme, name, label, kind):
    key, size, h = "sans-m", 15, 44
    tw = measure(label, key, size)
    w = round(tw + 16 + 10 + 22 * 2 + 18)
    s = Svg(w, h, label, theme)
    c = s.c
    s.add(f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{h / 2 - 0.5}" fill="{c["card"]}" stroke="{c["line2"]}"/>')
    if kind == "linkedin":
        s.icon("linkedin", 22, 14, 16, c["fg"])
    else:
        _glyph(s, kind, 22, 14, c["fg"])
    s.text(48, 27, label, key, size, c["fg"])
    # small north-east arrow
    ax = 48 + tw + 10
    s.add(f'<path d="M{ax} {27} L{ax + 7} {20} M{ax + 2} {20} H{ax + 7} V{25}" fill="none" stroke="{c["accent"]}" stroke-width="1.5" stroke-linecap="round"/>')
    s.save(f"chip-{name}")


# ---------------------------------------------------------------- section headers

def header(theme, name, index, title, sub, mobile=False):
    w = 600 if mobile else 1200
    s = Svg(w, 120 if mobile else 112, f"{title}: {sub}", theme)
    c = s.c
    ts = 30 if mobile else 30
    y = 62
    s.text(4, y, index, "mono-m", 14, c["accent"])
    tx = 4 + measure(index, "mono-m", 14) + 14
    s.text(tx, y + 1, title, "sans-sb", ts, c["fg"], tracking=-0.02)
    end = tx + measure(title, "sans-sb", ts, -0.02) + 20
    if mobile:
        s.text(4, y + 34, sub, "sans", 17, c["subtle"])
        s.add(f'<line x1="{end}" y1="{y - 9}" x2="{w - 4}" y2="{y - 9}" stroke="{c["line"]}"/>')
    else:
        s.text(end, y, sub, "sans", 17, c["subtle"])
        end2 = end + measure(sub, "sans", 17) + 24
        s.add(f'<line x1="{end2}" y1="{y - 6}" x2="{w - 4}" y2="{y - 6}" stroke="{c["line"]}"/>')
    s.save(f"h-{name}.m" if mobile else f"h-{name}")


# ---------------------------------------------------------------- experience

def experience(theme, job, mobile=False):
    title = f"{job['company']}: {job['role']}, {job['dates']}. {' '.join(job['points'])}"
    if not mobile:
        w = 1200
        pts = [wrap(p, "sans", 16, 640) for p in job["points"]]
        n = sum(len(x) for x in pts)
        h = max(250, 64 + n * 25 + (len(pts) - 1) * 10 + 32)
        s = Svg(w, h, title, theme)
        c = s.c
        s.frame(rx=18, glow=(0, 0, 460))
        lx = 36
        s.add(f'<rect x="{lx}" y="36" width="44" height="44" rx="12" fill="{c["card2"]}" stroke="{c["line"]}"/>')
        s.text(lx + 22, 63, job["region"], "mono-m", 14, c["accent"], anchor="middle")
        s.text(lx + 60, 54, job["company"], "sans-sb", 22, c["fg"], tracking=-0.01)
        s.text(lx + 60, 76, job["note"], "sans", 14, c["subtle"])
        s.text(lx, 124, job["role"], "sans-m", 16, c["fg"])
        s.text(lx, 148, f"{job['dates']} · Remote", "mono", 13, c["subtle"])
        cw = measure(f"{job['dates']} · Remote", "mono", 13)
        pulse_dot(s, lx + cw + 22, 143.5, c["green"], 3.5)
        s.text(lx + cw + 34, 148, "current", "mono", 13, c["green"])
        # tags
        tx, ty = lx, h - 60
        for t in job["tags"]:
            tx += s.pill(tx, ty, t) + 8
        # divider + bullets
        bx = 470
        s.add(f'<line x1="{bx - 36}" y1="36" x2="{bx - 36}" y2="{h - 36}" stroke="{c["line"]}"/>')
        y = 60
        for lines in pts:
            s.add(f'<path d="M{bx} {y - 9} l7 4.5 l-7 4.5" fill="none" stroke="{c["accent"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
            for line in lines:
                s.text(bx + 22, y, line, "sans", 16, c["muted"])
                y += 25
            y += 10
    else:
        w = 600
        pts = [wrap(p, "sans", 19, 500) for p in job["points"]]
        n = sum(len(x) for x in pts)
        tag_rows = 1
        h = 250 + n * 29 + len(pts) * 12 + tag_rows * 40
        s = Svg(w, h, title, theme)
        c = s.c
        s.frame(rx=18, glow=(0, 0, 360))
        lx = 30
        s.add(f'<rect x="{lx}" y="30" width="52" height="52" rx="13" fill="{c["card2"]}" stroke="{c["line"]}"/>')
        s.text(lx + 26, 61.5, job["region"], "mono-m", 16, c["accent"], anchor="middle")
        s.text(lx + 68, 52, job["company"], "sans-sb", 25, c["fg"], tracking=-0.01)
        s.text(lx + 68, 77, job["note"], "sans", 16, c["subtle"])
        s.text(lx, 126, job["role"], "sans-m", 19, c["fg"])
        s.text(lx, 154, f"{job['dates']} · Remote", "mono", 15, c["subtle"])
        y = 200
        for lines in pts:
            s.add(f'<path d="M{lx} {y - 11} l8 5 l-8 5" fill="none" stroke="{c["accent"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
            for line in lines:
                s.text(lx + 24, y, line, "sans", 19, c["muted"])
                y += 29
            y += 12
        tx = lx
        for t in job["tags"]:
            tx += s.pill(tx, y + 4, t, size=14, h=30, padx=12) + 8
    s.save(f"exp-{job['slug']}.m" if mobile else f"exp-{job['slug']}")


# ---------------------------------------------------------------- projects

def cover_glyph(s, kind, x, y, col, k=1.0):
    """Line drawings for the project icon tiles; (x, y) is the top-left of a 24*k box."""
    st = f'fill="none" stroke="{col}" stroke-width="{1.7}" stroke-linecap="round" stroke-linejoin="round"'
    g = f'<g transform="translate({x} {y}) scale({k})">'
    if kind == "billing":
        g += f'<path d="M5 2 H19 V22 L16.5 20 L14 22 L11.5 20 L9 22 L6.5 20 L5 21 Z" {st}/><path d="M8.5 7 H15.5 M8.5 11 H15.5 M8.5 15 H12.5" {st}/>'
    elif kind == "finance":
        g += f'<path d="M3 21 H21" {st}/><path d="M6 17 V13 M10.5 17 V9 M15 17 V11 M19.5 17 V5" {st}/><path d="M4 9 L9 5.5 L13 8 L20 2.5" {st}/>'
    elif kind == "marketplace":
        g += f'<path d="M4 7.5 H20 L18.8 21 H5.2 Z" {st}/><path d="M8.5 10 V6 a3.5 3.5 0 0 1 7 0 V10" {st}/>'
    elif kind == "stock":
        g += f'<path d="M3 13 H11 V21 H3 Z M13 13 H21 V21 H13 Z M8 4 H16 V12 H8 Z" {st}/><path d="M6 13 V16 M16 13 V16 M11 4 V7" {st}/>'
    s.add(g + "</g>")


LANG_COLOR = {"TypeScript": "#3178c6", "PHP": "#4F5D95", "Python": "#3572A5", "JavaScript": "#f1e05a", "Lua": "#000080"}


def project(theme, pr, mobile=False):
    link = f"github.com/{USER}/{pr['repo']}" if pr["repo"] else "private repository"
    title = f"{pr['title']}: {pr['summary']}"
    if not mobile:
        w, h = 600, 296
        s = Svg(w, h, title, theme)
        c = s.c
        s.frame(rx=18, glow=(0, 0, 340))
        s.add(f'<rect x="28" y="28" width="52" height="52" rx="13" fill="{c["card2"]}" stroke="{c["line"]}"/>')
        cover_glyph(s, pr["cover"], 42, 42, c["accent"])
        s.text(96, 51, pr["title"], "sans-sb", 19, c["fg"], tracking=-0.01)
        s.text(96, 73, link, "mono", 12, c["subtle"])
        lc = LANG_COLOR.get(pr["lang"], c["subtle"])
        if pr["lang"] == "Lua" and theme == "dark":
            lc = "#7c83ff"
        lw = measure(pr["lang"], "mono", 12)
        s.add(f'<circle cx="{w - 28 - lw - 12}" cy="{47}" r="5" fill="{lc}"/>')
        s.text(w - 28, 51, pr["lang"], "mono", 12, c["subtle"], anchor="end")
        y = 122
        for line in wrap(pr["summary"], "sans", 16, 544):
            s.text(28, y, line, "sans", 16, c["muted"])
            y += 24
        y += 12
        for i, hl in enumerate(pr["highlights"]):
            hx = 28 + (i % 2) * 272
            hy = y + (i // 2) * 30
            s.add(f'<path d="M{hx} {hy - 4.5} l3.5 3.5 l7 -7.5" fill="none" stroke="{c["accent"]}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>')
            s.text(hx + 20, hy, hl, "sans", 15, c["fg"])
        # tags, wrapping right-to-left up from the bottom edge
        rows, cur, cw = [], [], 0
        for t in pr["tags"]:
            tw = measure(t, "mono", 12) + 20
            if cur and cw + tw > 544:
                rows.append(cur)
                cur, cw = [], 0
            cur.append(t)
            cw += tw + 8
        rows.append(cur)
        ty = h - 28 - 24 - (len(rows) - 1) * 32
        for row in rows:
            tx = 28
            for t in row:
                tx += s.pill(tx, ty, t) + 8
            ty += 32
    else:
        w, h = 600, 600
        s = Svg(w, h, title, theme)
        c = s.c
        s.frame(rx=26, glow=(0, 0, 420))
        s.add(f'<rect x="40" y="40" width="96" height="96" rx="24" fill="{c["card2"]}" stroke="{c["line"]}"/>')
        cover_glyph(s, pr["cover"], 58, 58, c["accent"], 60 / 24)
        y = 230
        for line in wrap(pr["title"], "sans-sb", 46, 520):
            s.text(40, y, line, "sans-sb", 46, c["fg"], tracking=-0.02)
            y += 54
        y += 14
        for line in wrap(pr["summary"], "sans", 30, 520)[:3]:
            s.text(40, y, line, "sans", 30, c["muted"])
            y += 40
        s.text(40, h - 44, pr["lang"], "mono", 26, c["subtle"])
    s.save(f"proj-{pr['slug']}.m" if mobile else f"proj-{pr['slug']}")


# ---------------------------------------------------------------- stack

def tile_glyph(s, slug, cx, cy, size):
    c = s.c
    if not slug.startswith("@"):
        s.icon(slug, cx - size / 2, cy - size / 2, size, brand(s, slug))
        return
    kind = slug[1:]
    col = c["accent"]
    st = f'fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    k = size / 24
    x, y = cx - size / 2, cy - size / 2
    g = f'<g transform="translate({x:.1f} {y:.1f}) scale({k:.3f})">'
    if kind == "sql":
        g += f'<ellipse cx="12" cy="5" rx="8" ry="3" {st}/><path d="M4 5 V19 c0 1.7 3.6 3 8 3 s8 -1.3 8 -3 V5 M4 12 c0 1.7 3.6 3 8 3 s8 -1.3 8 -3" {st}/>'
    elif kind == "table":
        g += f'<rect x="3" y="4" width="18" height="16" rx="2.5" {st}/><path d="M3 9.5 H21 M3 14.75 H21 M9.5 9.5 V20" {st}/>'
    elif kind == "route":
        g += f'<path d="M3 12 H9 L14 6 H21 M9 12 L14 18 H21 M18 3 L21 6 L18 9 M18 15 L21 18 L18 21" {st}/>'
    elif kind == "spark":
        g += f'<path d="M12 3 L13.8 9.2 L20 11 L13.8 12.8 L12 19 L10.2 12.8 L4 11 L10.2 9.2 Z" {st}/><path d="M19 3 V6 M17.5 4.5 H20.5" {st}/>'
    elif kind == "bars":
        g += f'<path d="M3 21 H21 M6.5 17 V11 M11 17 V6 M15.5 17 V13 M20 17 V8" {st}/>'
    elif kind == "rest":
        g += f'<path d="M8 3 C5 3 5 5 5 8 S4 12 3 12 C4 12 5 13 5 16 S5 21 8 21 M16 3 C19 3 19 5 19 8 S20 12 21 12 C20 12 19 13 19 16 S19 21 16 21" {st}/>'
    elif kind == "lock":
        g += f'<rect x="4.5" y="10.5" width="15" height="11" rx="2.5" {st}/><path d="M8 10.5 V7 a4 4 0 0 1 8 0 V10.5 M12 15 V17" {st}/>'
    elif kind == "nui":
        g += f'<rect x="2.5" y="4" width="19" height="16" rx="2.5" {st}/><path d="M2.5 8.5 H21.5 M9 12.5 L6.5 15 L9 17.5 M15 12.5 L17.5 15 L15 17.5" {st}/>'
    elif kind == "code":
        g += f'<path d="M8 6 L2 12 L8 18 M16 6 L22 12 L16 18 M14 4 L10 20" {st}/>'
    s.add(g + "</g>")


def stack(theme, mobile=False):
    names = ", ".join(n for _, _, items in STACK for n, _ in items)
    if not mobile:
        tw_, th_, gap = 100, 92, 10
        row_h = th_ + 36
        w, h = 1200, len(STACK) * row_h + 24
        s = Svg(w, h, f"Stack: {names}", theme)
        c = s.c
        s.frame(rx=20)
        for r, (group, cap, items) in enumerate(STACK):
            y0 = 12 + r * row_h
            if r:
                s.add(f'<line x1="24" y1="{y0}" x2="{w - 24}" y2="{y0}" stroke="{c["line"]}"/>')
            s.text(40, y0 + row_h / 2 - 3, group, "sans-sb", 17, c["fg"])
            s.text(40, y0 + row_h / 2 + 19, cap, "sans", 14, c["subtle"])
            for i, (label, slug) in enumerate(items):
                x = 400 + i * (tw_ + gap)
                y = y0 + (row_h - th_) / 2
                s.add(f'<rect x="{x}" y="{y}" width="{tw_}" height="{th_}" rx="14" fill="{c["card2"]}" stroke="{c["line"]}"/>')
                tile_glyph(s, slug, x + tw_ / 2, y + 36, 28)
                s.text(x + tw_ / 2, y + 74, label, "mono", 11.5, c["muted"], anchor="middle")
    else:
        tw_, th_, gap, per = 98, 98, 10, 5
        y = 30
        rows = []
        for group, cap, items in STACK:
            nrows = -(-len(items) // per)
            rows.append((y, group, cap, items))
            y += 74 + nrows * (th_ + gap) + 22
        w, h = 600, y + 8
        s = Svg(w, h, f"Stack: {names}", theme)
        c = s.c
        s.frame(rx=20)
        for r, (y0, group, cap, items) in enumerate(rows):
            if r:
                s.add(f'<line x1="24" y1="{y0 - 18}" x2="{w - 24}" y2="{y0 - 18}" stroke="{c["line"]}"/>')
            s.text(30, y0 + 22, group, "sans-sb", 21, c["fg"])
            s.text(30, y0 + 50, cap, "sans", 16, c["subtle"])
            for i, (label, slug) in enumerate(items):
                x = 30 + (i % per) * (tw_ + gap)
                yy = y0 + 70 + (i // per) * (th_ + gap)
                s.add(f'<rect x="{x}" y="{yy}" width="{tw_}" height="{th_}" rx="16" fill="{c["card2"]}" stroke="{c["line"]}"/>')
                tile_glyph(s, slug, x + tw_ / 2, yy + 40, 32)
                s.text(x + tw_ / 2, yy + 82, label, "mono", 13, c["muted"], anchor="middle")
    s.save("stack.m" if mobile else "stack")


# ---------------------------------------------------------------- footer

def footer(theme, mobile=False):
    w = 600 if mobile else 1200
    s = Svg(w, 96, "Made in Ahmedabad, India.", theme)
    c = s.c
    cx = w / 2
    s.add(f'<line x1="{cx - 160}" y1="30" x2="{cx - 18}" y2="30" stroke="{c["line"]}"/><line x1="{cx + 18}" y1="30" x2="{cx + 160}" y2="30" stroke="{c["line"]}"/>')
    s.add(f'<rect x="{cx - 5}" y="25" width="10" height="10" transform="rotate(45 {cx} 30)" fill="{c["accent"]}"/>')
    s.runs(cx, 72, [("Made in ", "sans", c["subtle"]), ("Ahmedabad", "serif", c["fg"]), (", India.", "sans", c["subtle"])], 20 if mobile else 18, anchor="middle")
    s.save("footer.m" if mobile else "footer")


def build_all():
    for theme in ("dark", "light"):
        for m in (False, True):
            hero(theme, m)
            stack(theme, m)
            footer(theme, m)
            for job in EXPERIENCE if SHOW_WORK else []:
                experience(theme, job, m)
            for pr in PROJECTS:
                project(theme, pr, m)
            for name, idx, title, sub in HEADERS:
                header(theme, name, idx, title, sub, m)
        chip(theme, "linkedin", "LinkedIn", "linkedin")
        chip(theme, "email", "Email me", "mail")
        chip(theme, "portfolio", "mihir0336.vercel.app", "globe")
        chip(theme, "resume", "Resume", "doc")


HEADERS = [
    ("work", "Work", "Paid to ship for live GTA V roleplay servers"),
    ("projects", "Projects", "Full-stack apps I've built end to end"),
    ("stack", "Stack", "What my work is made of"),
    ("activity", "Activity", "Every contribution in the last year"),
]
if not SHOW_WORK:
    HEADERS = HEADERS[1:]
# number the sections that are actually shown: ("projects", "01", ...)
HEADERS = [(name, f"{i:02}", title, sub) for i, (name, title, sub) in enumerate(HEADERS, 1)]
