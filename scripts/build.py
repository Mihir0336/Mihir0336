"""Builds every card in assets/{dark,light} and writes README.md.

    python scripts/build.py           # everything
    python scripts/build.py --static  # skip the live activity card (no network)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import activity  # noqa: E402
import cards  # noqa: E402
from content import EXPERIENCE, PROFILE, PROJECTS, USER  # noqa: E402
from kit import ROOT  # noqa: E402


def pic(name, alt, width="100%", mobile=True):
    """<picture> that swaps dark/light and, when there is one, the narrow-screen variant."""
    src = []
    if mobile:
        src.append(f'<source media="(prefers-color-scheme: dark) and (max-width: 640px)" srcset="assets/dark/{name}.m.svg">')
        src.append(f'<source media="(max-width: 640px)" srcset="assets/light/{name}.m.svg">')
    src.append(f'<source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg">')
    w = f' width="{width}"' if width else ""
    return f'<picture>{"".join(src)}<img src="assets/light/{name}.svg"{w} alt="{alt}"></picture>'


def readme():
    p = PROFILE
    out = ['<div align="center">', ""]
    out.append(pic("hero", f"{p['name']}, {p['role']}. {p['pitch']}"))
    out += ["", "<p>", "Next.js, React and TypeScript on the web,<br>", "Lua and NUI inside live GTA V roleplay servers.<br>",
            "Based in Ahmedabad, open to full-time roles.", "</p>", ""]
    chips = [
        (p["linkedin"], "linkedin", "LinkedIn"),
        (f"mailto:{p['email']}", "email", "Email me"),
        (p["site"], "portfolio", "mihir0336.vercel.app"),
        (p["resume"], "resume", "Resume"),
    ]
    for href, name, alt in chips:
        out.append(f'<a href="{href}">{pic(f"chip-{name}", alt, width=None, mobile=False)}</a>')
    out += ["", "<br><br>", ""]

    out.append(pic("h-work", "Work: Paid to ship for live GTA V roleplay servers"))
    out.append("")
    for job in EXPERIENCE:
        out.append(pic(f"exp-{job['slug']}", f"{job['company']}, {job['role']}, {job['dates']}"))
        out.append("")
    out += ["<br>", ""]

    out.append(pic("h-projects", "Projects: Full-stack apps I've built end to end"))
    out.append("")
    for i, pr in enumerate(PROJECTS):
        href = f"https://github.com/{USER}/{pr['repo']}" if pr["repo"] else pr["href"]
        card = pic(f"proj-{pr['slug']}", f"{pr['title']}: {pr['summary']}", width="49%")
        out.append(f'<a href="{href}">{card}</a>')
        if i % 2 == 1 and i != len(PROJECTS) - 1:
            out.append("<br>")
    out += ["", "<br><br>", ""]

    out.append(pic("h-stack", "Stack: What my work is made of"))
    out.append("")
    out.append(pic("stack", "Stack: JavaScript, TypeScript, Lua, PHP, SQL, React, Next.js, Svelte, Tailwind, Node.js, Express, Prisma, MySQL, MongoDB, FiveM, Git, Vercel"))
    out += ["", "<br><br>", ""]

    out.append(pic("h-activity", "Activity: Every contribution in the last year"))
    out.append("")
    out.append(pic("activity", "Contribution calendar, streaks and languages"))
    out.append("")
    out.append(pic("footer", "Made in Ahmedabad, India."))
    out += ["", "</div>", ""]
    (ROOT / "README.md").write_text("\n".join(out), encoding="utf-8")


def main():
    cards.build_all()
    if "--static" not in sys.argv:
        try:
            days, langs = activity.build_all()
            print(f"activity: {sum(d[1] for d in days)} contributions, {len(langs)} languages")
        except Exception as e:  # keep the last good activity card rather than failing the run
            print(f"activity skipped: {e}")
    readme()
    print("done")


if __name__ == "__main__":
    main()
