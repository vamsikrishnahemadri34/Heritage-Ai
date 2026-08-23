import json
import re
from sqlalchemy import create_engine, text
from app.core.config import settings

def clean(value):
    return re.sub(r"<[^>]+>", "", value or "").strip()

def slugify(value):
    value = clean(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")

with open("heritage_89_candidates.json", encoding="utf-8") as f:
    candidates = json.load(f)

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    rows = conn.execute(
        text("""
            SELECT name, slug
            FROM heritage_sites
        """)
    ).fetchall()

existing_names = {clean(row.name).lower() for row in rows}
existing_slugs = {row.slug for row in rows}

duplicates = []

for site in candidates:
    name = clean(site["name"])
    slug = slugify(name)

    if name.lower() in existing_names:
        duplicates.append(
            ("NAME", name, site["country"])
        )
    elif slug in existing_slugs:
        duplicates.append(
            ("SLUG", name, site["country"])
        )

print("CANDIDATES:", len(candidates))
print("EXISTING DATABASE SITES:", len(rows))
print("DUPLICATES FOUND:", len(duplicates))
print()

for kind, name, country in duplicates:
    print(f"{kind}: {name} | {country}")

print()

if not duplicates:
    print("NO DATABASE DUPLICATES FOUND.")
else:
    print("IMPORT MUST NOT RUN YET.")
