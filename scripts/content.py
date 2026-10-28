"""Everything the cards say. Source of truth is the resume (Mihir_Patel_CV.pdf, updated 2026-10-28)."""

USER = "Mihir0336"

PROFILE = {
    "name": "Mihir Patel",
    "role": "Full Stack Developer",
    "location": "Ahmedabad, IN",
    "pitch": (
        "I build full-stack web apps with React, Next.js and TypeScript. For 1+ year I've "
        "shipped production features remotely, for a US-based gaming platform and a "
        "freelance client's WhatsApp marketing SaaS."
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
        "note": "US-based multiplayer GTA V roleplay server",
        "region": "US",
        "role": "Full Stack Developer",
        "dates": "Aug 2025 – Present",
        "points": [
            "Build in-game user interfaces in React and Svelte for a live multiplayer GTA V roleplay server.",
            "Write client- and server-side logic in Lua and connect it to the React/Svelte frontends through FiveM NUI.",
            "Ship features to a live production server, working remotely with the US-based owners across time zones.",
        ],
        "tags": ["React", "Svelte", "Lua", "FiveM", "NUI"],
    },
    {
        "slug": "whatsapp-saas",
        "company": "WhatsApp Marketing Platform",
        "note": "Freelance client project",
        "region": "FL",
        "role": "Full Stack Developer",
        "dates": "May 2026 – Jun 2026",
        "points": [
            "Customized and extended a production WhatsApp marketing SaaS built on React, TypeScript, Express and PostgreSQL.",
            "Shipped template rotation, per-account channel limits, group exclusion and reply tracking with Excel exports.",
            "Deployed and maintained it on a Linux VPS with Nginx and PM2, including schema migrations.",
        ],
        "tags": ["React", "TypeScript", "Express", "PostgreSQL", "Redis"],
    },
]

PROJECTS = [
    {
        "slug": "inventory-billing",
        "title": "Inventory & Billing System",
        "summary": "Full-stack inventory and billing app with an analytics dashboard.",
        "highlights": ["NextAuth authentication", "Stock tracking", "GST-inclusive bills", "Dashboard, dark/light mode"],
        "tags": ["Next.js", "TypeScript", "MySQL", "NextAuth", "Tailwind CSS"],
        "cover": "billing",
        "lang": "TypeScript",
        "repo": None,  # private for now
        "href": "https://mihir0336.vercel.app/#projects",
    },
    {
        "slug": "finance-visualizer",
        "title": "Personal Finance Visualizer",
        "summary": "Finance tracker with budgets and monthly charts on MongoDB Atlas.",
        "highlights": ["7 REST endpoints", "Category budgets", "Auto-refresh, cross-tab sync", "Paginated loading"],
        "tags": ["Next.js", "TypeScript", "MongoDB", "shadcn/ui"],
        "cover": "finance",
        "lang": "TypeScript",
        "repo": "finance-visualizer",
    },
    {
        "slug": "unimart",
        "title": "UniMart, University Marketplace",
        "summary": "Multi-role marketplace with separate admin, seller and buyer portals.",
        "highlights": ["Search, cart, coupons", "Order tracking", "Admin moderation", "SQLi and XSS protection"],
        "tags": ["PHP", "MySQL", "JavaScript", "AJAX", "Bootstrap"],
        "cover": "marketplace",
        "lang": "PHP",
        "repo": "UniMart-Groceries",
    },
]

# (label, simple-icons slug or a built-in glyph name)
STACK = [
    ("Languages", "What I build with", [
        ("JavaScript", "javascript"), ("TypeScript", "typescript"), ("Python", "python"), ("PHP", "php"),
        ("Lua", "lua"), ("SQL", "@table"), ("HTML/CSS", "html5"),
    ]),
    ("Frontend", "Interfaces on the web and in game", [
        ("React", "react"), ("Next.js", "nextdotjs"), ("Svelte", "svelte"), ("Tailwind", "tailwindcss"),
        ("shadcn/ui", "shadcnui"),
    ]),
    ("Backend & data", "APIs, auth and storage", [
        ("Node.js", "nodedotjs"), ("API routes", "@route"), ("REST", "@rest"), ("NextAuth", "@lock"),
        ("MySQL", "@sql"), ("MongoDB", "mongodb"),
    ]),
    ("Tools & deploy", "From commit to a live server", [
        ("Git", "git"), ("GitHub", "github"), ("Vercel", "vercel"), ("Linux VPS", "linux"),
        ("Nginx", "nginx"), ("PM2", "pm2"), ("AI tools", "@spark"),
    ]),
]

EDUCATION = "B.E. Computer Engineering, Monark University"
