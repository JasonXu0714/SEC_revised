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

# Intangible_keywords = ["intangible"]
Intangible_keywords = [
    "intangible",
    "employee",
    "customer",
    "data",
    "abilit",
    "system",
    "marketing",
    "technology",
    "research",
    "intellectual property",
    "software",
    "consumer",
    "advertising",
    "relationship",
    "ability",
    "experience",
    "expertise",
    "talent",
    "customer",
    "algorithm",
    "authorship",
    "brand",
    "client",
    "competenc",
    "connecti",
    "copyright",
    "design",
    "discovery",
    "exper",
    "formula",
    "franchise",
    "human",
    "innovat",
    "intellectual",
    "internet",
    "invent",
    "know",
    "label",
    "licence",
    "logo",
    "loyalty",
    "names",
    "network",
    "patent",
    "platform",
    "presence",
    "product",
    "register",
    "relation",
    "reputation",
    "site visits",
    "skill",
    "solution"]



root_directory = os.getcwd()
data_directory = os.path.join(root_directory, "data")
