import json
import re
import uuid
from datetime import datetime

from sqlalchemy import create_engine, text

from app.core.config import settings


INPUT_FILE = "heritage_89_candidates.json"


def clean(value):
    if not value:
        return None

    value = re.sub(r"<[^>]+>", "", str(value))
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def make_slug(value):
    value = clean(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


with open(INPUT_FILE, encoding="utf-8") as f:
    candidates = json.load(f)


engine = create_engine(settings.DATABASE_URL)

inserted = 0
skipped = 0

now = datetime.utcnow()


with engine.begin() as conn:

    existing = conn.execute(
        text("""
            SELECT name, slug
            FROM heritage_sites
        """)
    ).fetchall()

    existing_names = {
        clean(row.name).lower()
        for row in existing
    }

    existing_slugs = {
        row.slug
        for row in existing
    }

    for site in candidates:

        name = clean(site.get("name"))
        slug = make_slug(name)

        if not name:
            skipped += 1
            continue

        if (
            name.lower() in existing_names
            or slug in existing_slugs
        ):
            skipped += 1
            continue

        description = clean(site.get("description"))

        category = clean(site.get("category")) or "Cultural"

        country = clean(site.get("country")) or "Unknown"

        established_year = None

        if site.get("date_inscribed"):
            try:
                established_year = int(
                    str(site["date_inscribed"])[:4]
                )
            except (ValueError, TypeError):
                established_year = None

        conn.execute(
            text("""
                INSERT INTO heritage_sites (
                    id,
                    name,
                    slug,
                    short_description,
                    description,
                    category,
                    country,
                    state,
                    city,
                    latitude,
                    longitude,
                    established_year,
                    architectural_style,
                    historical_period,
                    significance,
                    preservation_status,
                    is_verified,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (
                    :id,
                    :name,
                    :slug,
                    :short_description,
                    :description,
                    :category,
                    :country,
                    NULL,
                    NULL,
                    :latitude,
                    :longitude,
                    :established_year,
                    NULL,
                    NULL,
                    NULL,
                    NULL,
                    :is_verified,
                    :is_active,
                    :created_at,
                    :updated_at
                )
            """),
            {
                "id": str(uuid.uuid4()),
                "name": name,
                "slug": slug,
                "short_description": (
                    description[:500]
                    if description
                    else None
                ),
                "description": description,
                "category": category,
                "country": country,
                "latitude": site.get("latitude"),
                "longitude": site.get("longitude"),
                "established_year": established_year,
                "is_verified": False,
                "is_active": True,
                "created_at": now,
                "updated_at": now,
            },
        )

        inserted += 1

        existing_names.add(name.lower())
        existing_slugs.add(slug)


print("========================================")
print("HERITAGEAI UNESCO IMPORT")
print("========================================")
print()
print("Candidates :", len(candidates))
print("Inserted   :", inserted)
print("Skipped    :", skipped)
print()
print("Import completed successfully.")
