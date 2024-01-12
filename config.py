import os

START_YEAR = 2016
END_YEAR = 2016
FILE_NAME = "filing_attachment"
COLUMN_NAMES = [
    "company_name",
    "filing_date",
    "cik",
    "trade_secrets",
    "net_trade_secrets",
    "indicator",
    "url",
    "accession_no",
]

Intangible_keywords = ["intangible"]
# Intangible_keywords = [
#     "intangible assets",
#     "intangible",
#     "customer relationship",
#     "relationship",
#     "abilities",
#     "customer",
#     "relation",
#     "innovation",
#     "networks",
#     "talent",
#     "ability",
#     "customers",
#     "innovations",
#     "patent",
#     "talents",
#     "advertising",
#     "data",
#     "innovator",
#     "patented",
#     "team",
#     "algorithm",
#     "database",
#     "innovators",
#     "patents",
#     "teams",
#     "authorship",
#     "databases",
#     "intellectual",
#     "platform",
#     "teamwork",
#     "authorships",
#     "design",
#     "intellectual property",
#     "platforms",
#     "technologies",
#     "brand",
#     "designs",
#     "intellectual property",
#     "presence",
#     "technology",
#     "branding",
#     "discoveries",
#     "internet",
#     "productivity",
#     "trade mark",
#     "brands",
#     "discovery",
#     "internet activities",
#     "protected design",
#     "trade marks",
#     "client",
#     "employee",
#     "internet activity",
#     "protected designs",
#     "trade name",
#     "client relations",
#     "employees",
#     "invent",
#     "registered design",
#     "trade secret",
#     "clients",
#     "experience",
#     "invented",
#     "registered designs",
#     "trade secrets",
#     "competence",
#     "expert",
#     "inventing",
#     "relation",
#     "trademark",
#     "competences",
#     "expertise",
#     "invention",
#     "relations",
#     "trademarks",
#     "competencies",
#     "experts",
#     "inventions",
#     "relationship",
#     "training",
#     "competency",
#     "formula",
#     "invents",
#     "relationships",
#     "user",
#     "connections",
#     "formulae",
#     "knowhow",
#     "reputation",
#     "users",
#     "connectivity",
#     "franchise",
#     "knowledge",
#     "research",
#     "website",
#     "consumer",
#     "franchises",
#     "label",
#     "researches",
#     "websites",
#     "consumers",
#     "human",
#     "labels",
#     "site",
#     "visits",
#     "workforce",
#     "copyright",
#     "human capital",
#     "licence",
#     "skill",
#     "copyrights",
#     "human resources",
#     "licences",
#     "skills",
#     "customer",
#     "innovate",
#     "logo",
#     "software",
#     "customer base",
#     "innovate partners",
#     "loyalty",
#     "solution",
#     "customer bases",
#     "innovated",
#     "marketing",
#     "solutions",
#     "customer list",
#     "innovates",
#     "names",
#     "system",
#     "customer lists",
#     "innovating",
#     "network",
#     "systems",
# ]


root_directory = os.getcwd()
