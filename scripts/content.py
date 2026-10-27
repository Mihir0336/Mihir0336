"""Everything the cards say. Mirrors src/content.ts in the portfolio repo; keep the two in sync."""

USER = "Mihir0336"

PROFILE = {
    "name": "Mihir Patel",
    "role": "Full Stack Developer",
    "location": "Ahmedabad, IN",
    "pitch": (
        "I build full-stack web apps with Next.js, React and TypeScript, and for 1+ year "
        "I've been paid to ship gameplay systems and in-game UIs remotely for two live "
        "GTA V roleplay communities."
    ),
    "email": "mihirpatel0336@gmail.com",
    "site": "https://mihir0336.vercel.app",
    "resume": "https://mihir0336.vercel.app/Mihir_Patel_CV.pdf",
    "linkedin": "https://www.linkedin.com/in/mihirpatel0336",
}

# The Work section (experience cards) is hidden on the profile; flip to True to bring it back.
SHOW_WORK = False

EXPERIENCE = [
    {
        "slug": "legacy-network",
        "company": "Legacy Network",
        "note": "US-based GTA V roleplay server",
        "region": "US",
        "role": "Full Stack Developer",
        "dates": "Aug 2025 – Present",
        "points": [
            "Build custom FiveM gameplay scripts in Lua, on both the client and server side.",
            "Build in-game UIs in React and Svelte, connected to Lua through FiveM's NUI messaging.",
            "Work remotely with the server owners across time zones.",
        ],
        "tags": ["Lua", "React", "Svelte", "FiveM", "NUI"],
    },
    {
        "slug": "yatra-roleplay",
        "company": "Yatra Roleplay",
        "note": "Indian GTA V roleplay server",
        "region": "IN",
        "role": "Full Stack Developer",
        "dates": "Aug 2025 – Present",
        "points": [
            "Write custom Lua scripts and React/Svelte interfaces.",
            "Ship features for two live communities in parallel.",
        ],
        "tags": ["Lua", "React", "Svelte", "FiveM"],
    },
]

PROJECTS = [
    {
        "slug": "inventory-billing",
        "title": "Inventory & Billing System",
        "summary": "Full-stack inventory and billing app with an analytics dashboard.",
        "highlights": ["Authentication", "Stock tracking", "GST-inclusive billing", "Dashboard with charts"],
        "tags": ["Next.js", "TypeScript", "Prisma ORM", "MySQL", "NextAuth", "Tailwind CSS"],
        "cover": "billing",
        "lang": "TypeScript",
        "repo": None,  # private for now
        "href": "https://mihir0336.vercel.app/#projects",
    },
    {
        "slug": "finance-visualizer",
        "title": "Personal Finance Visualizer",
        "summary": "Personal finance tracker with budgets and monthly charts.",
        "highlights": ["7 REST endpoints", "Monthly charts", "Budgets", "Cross-tab sync"],
        "tags": ["Next.js 14", "TypeScript", "MongoDB", "Recharts", "shadcn/ui"],
        "cover": "finance",
        "lang": "TypeScript",
        "repo": "finance-visualizer",
    },
    {
        "slug": "unimart",
        "title": "UniMart, University Marketplace",
        "summary": "University marketplace with separate admin, seller and buyer portals.",
        "highlights": ["Three role portals", "Cart and coupons", "Order tracking", "SQLi and XSS protection"],
        "tags": ["PHP", "MySQL", "JavaScript", "jQuery/AJAX", "Bootstrap"],
        "cover": "marketplace",
        "lang": "PHP",
        "repo": "UniMart-Groceries",
    },
    {
        "slug": "stock-management",
        "title": "Stock Management System",
        "summary": "Inventory and GST billing system built for Agricon Shop.",
        "highlights": ["Inventory management", "GST billing", "Admin panel"],
        "tags": ["PHP", "MySQL", "JavaScript"],
        "cover": "stock",
        "lang": "PHP",
        "repo": "Stock-Management-System",
    },
]

# (label, simple-icons slug or a built-in glyph name)
STACK = [
    ("Languages", "What I write every day", [
        ("JavaScript", "javascript"), ("TypeScript", "typescript"), ("Lua", "lua"), ("PHP", "php"),
        ("SQL", "@table"), ("HTML", "html5"), ("CSS", "css3"),
    ]),
    ("Frontend", "Interfaces on the web and in game", [
        ("React", "react"), ("Next.js", "nextdotjs"), ("Svelte", "svelte"), ("Tailwind", "tailwindcss"),
        ("shadcn/ui", "shadcnui"), ("Framer", "framer"), ("Recharts", "@bars"),
    ]),
    ("Backend & data", "APIs, auth and storage", [
        ("Node.js", "nodedotjs"), ("Express", "express"), ("REST", "@rest"), ("NextAuth", "@lock"),
        ("Prisma", "prisma"), ("MySQL", "@sql"), ("MongoDB", "mongodb"),
    ]),
    ("Game dev & tools", "FiveM, NUI and shipping", [
        ("FiveM", "fivem"), ("NUI", "@nui"), ("Git", "git"), ("GitHub", "github"),
        ("Vercel", "vercel"), ("VS Code", "@code"),
    ]),
]

EDUCATION = "B.E. Computer Engineering, Monark University"
