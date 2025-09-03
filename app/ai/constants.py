

CANDIDATE_LABELS = [
    "React", "Vue", "Angular", "Svelte", "Next.js", "Nuxt.js",
    "Laravel", "Django", "Express", "Flask", "Spring Boot", "Node.js", "PHP", "Ruby on Rails", "ASP.NET",
    "Postgres", "MySQL", "MariaDB", "MongoDB", "DynamoDB", "Firebase", "SQLite",
    "AWS", "Azure", "GCP", "DigitalOcean", "on-prem", "Kubernetes", "Docker", "Serverless",
    "Stripe", "PayPal", "local banks", "payment gateway", "PCI-DSS",
    "Responsive Design", "Mobile-first", "PWA", "Accessibility", "RTL",
    "REST API", "GraphQL", "WebSocket", "Webhooks",
    "D3.js", "Chart.js", "Highcharts",
    "Cypress", "Playwright", "Jest", "PHPUnit", "CI/CD", "Terraform",
    "S3", "CDN", "Object storage", "Image optimization",
    "GDPR", "HIPAA", "OWASP", "WAF",
    "React Native", "Flutter", "iOS", "Android",
    "Payments", "Authentication", "OAuth", "SSO", "Two-factor", "2FA", "Email verification"
]

LABEL_TO_TOPIC = {
    "React": ("framework_frontend", "React"),
    "Vue": ("framework_frontend", "Vue"),
    "Angular": ("framework_frontend", "Angular"),
    "Svelte": ("framework_frontend", "Svelte"),
    "Next.js": ("framework_frontend", "Next.js"),
    "Nuxt.js": ("framework_frontend", "Nuxt.js"),
    "Laravel": ("framework_backend", "Laravel"),
    "Django": ("framework_backend", "Django"),
    "Express": ("framework_backend", "Express"),
    "Flask": ("framework_backend", "Flask"),
    "Spring Boot": ("framework_backend", "Spring Boot"),
    "Node.js": ("framework_backend", "Node.js"),
    "PHP": ("framework_backend", "PHP"),
    "Ruby on Rails": ("framework_backend", "Ruby on Rails"),
    "ASP.NET": ("framework_backend", "ASP.NET"),
    "Postgres": ("database", "Postgres"),
    "MySQL": ("database", "MySQL"),
    "MariaDB": ("database", "MariaDB"),
    "MongoDB": ("database", "MongoDB"),
    "DynamoDB": ("database", "DynamoDB"),
    "Firebase": ("database", "Firebase"),
    "SQLite": ("database", "SQLite"),
    "AWS": ("hosting", "AWS"),
    "Azure": ("hosting", "Azure"),
    "GCP": ("hosting", "GCP"),
    "DigitalOcean": ("hosting", "DigitalOcean"),
    "on-prem": ("hosting", "on-prem"),
    "Kubernetes": ("infrastructure", "Kubernetes"),
    "Docker": ("infrastructure", "Docker"),
    "Serverless": ("infrastructure", "Serverless"),
    "Stripe": ("payments", "Stripe"),
    "PayPal": ("payments", "PayPal"),
    "payment gateway": ("payments", "payment gateway"),
    "Payments": ("payments", "Payments"),
    "PCI-DSS": ("security_compliance", "PCI-DSS"),
    "Responsive Design": ("design_responsive", "Responsive"),
    "Mobile-first": ("design_responsive", "Mobile-first"),
    "PWA": ("mobile", "PWA"),
    "Accessibility": ("accessibility", "a11y"),
    "RTL": ("design_responsive", "RTL"),
    "REST API": ("apis", "REST"),
    "GraphQL": ("apis", "GraphQL"),
    "WebSocket": ("realtime", "WebSocket"),
    "Webhooks": ("apis", "Webhooks"),
    "D3.js": ("frontend_lib", "D3.js"),
    "Chart.js": ("frontend_lib", "Chart.js"),
    "Highcharts": ("frontend_lib", "Highcharts"),
    "Cypress": ("testing", "Cypress"),
    "Playwright": ("testing", "Playwright"),
    "Jest": ("testing", "Jest"),
    "PHPUnit": ("testing", "PHPUnit"),
    "CI/CD": ("devops", "CI/CD"),
    "Terraform": ("devops", "Terraform"),
    "S3": ("storage", "S3"),
    "CDN": ("storage", "CDN"),
    "Object storage": ("storage", "Object storage"),
    "Image optimization": ("storage", "Image optimization"),
    "GDPR": ("security_compliance", "GDPR"),
    "HIPAA": ("security_compliance", "HIPAA"),
    "OWASP": ("security_compliance", "OWASP"),
    "WAF": ("security_compliance", "WAF"),
    "React Native": ("mobile", "React Native"),
    "Flutter": ("mobile", "Flutter"),
    "iOS": ("mobile", "iOS"),
    "Android": ("mobile", "Android"),
    "Authentication": ("auth", "Authentication"),
    "OAuth": ("auth", "OAuth"),
    "SSO": ("auth", "SSO"),
    "Two-factor": ("auth", "2FA"),
    "2FA": ("auth", "2FA"),
    "Email verification": ("auth", "email verification"),
}

QUESTION_TEMPLATES = {
    "auth": [
        "What user registration and authentication methods are required? (email/password, OAuth/social login like Google/Facebook, phone/SMS, SSO).",
        "Should password recovery, email verification, or multi-factor authentication be implemented?"
    ],
    "database": [
        "Which database type do you prefer? (SQL: Postgres/MySQL, NoSQL: MongoDB/DynamoDB)? Specify version if known.",
        "Do you need replication, read-replicas, sharding, or strict ACID transactions?"
    ],
    "framework": [
        "Which backend and frontend frameworks should we use? (e.g., Laravel + React).",
        "If none provided, should the technical lead propose a stack?"
    ],
    "infrastructure": [
        "Where will the app be hosted? (AWS, Azure, GCP, DigitalOcean, or on-prem?).",
        "Do you need Docker, Kubernetes, serverless, or VMs?"
    ],
    "payments": [
        "What payment gateways should be integrated? (Stripe, PayPal, local bank?).",
        "Do you need recurring payments, refunds, or multi-currency?"
    ],
    "design": [
        "Should the site be mobile-first / responsive? Any target device priorities?",
        "Do you need a logo / brand kit? Who supplies them?"
    ],
    "apis": [
        "Will the project expose or require APIs (REST, GraphQL)? Do you need API docs (OpenAPI)?"
    ],
    "realtime": [
        "Do you need real-time features? (WebSocket, push updates, live notifications)?"
    ],
    "notifications": [
        "Should the system send notifications? (Email, SMS, push notifications)?",
        "Do you need in-app notifications or alerts?"
    ],
    "testing": [
        "What testing strategies do you prefer? (unit, integration, e2e, load)."
    ],
    "devops": [
        "Do you require CI/CD pipelines or infrastructure-as-code?"
    ],
   
}

DEFAULT_WEIGHTS = {"w_match": 1.0, "w_experience": 1.0, "w_availability": 1.0, "w_load_penalty": 0.5}

GA_CONFIG = {
    "population_size": 30,
    "generations": 60,
    "mutation_rate": 0.25,
    "elite_frac": 0.15,
}