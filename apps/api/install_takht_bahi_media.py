import uuid
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, text

from app.core.config import settings


SLUG = "buddhist-ruins-of-takht-i-bahi-and-neighbouring-city-remains-at-sahr-i-bahlol"
SOURCE = Path("takht_bahi.jpg")

MEDIA_ROOT = Path(settings.MEDIA_STORAGE_PATH)
BASE_URL = settings.MEDIA_BASE_URL.rstrip("/")

STORAGE_KEY = f"heritage/{SLUG}/{SLUG}-primary.jpg"


if not SOURCE.exists():
    raise RuntimeError("takht_bahi.jpg was not found.")

content = SOURCE.read_bytes()

if not content:
    raise RuntimeError("takht_bahi.jpg is empty.")

engine = create_engine(settings.DATABASE_URL)

with engine.begin() as conn:

    site = conn.execute(
        text("""
            SELECT id, name, country
            FROM heritage_sites
            WHERE slug = :slug
            LIMIT 1
        """),
        {"slug": SLUG},
    ).mappings().first()

    if not site:
        raise RuntimeError("Heritage site was not found.")

    existing = conn.execute(
        text("""
            SELECT id
            FROM heritage_site_media
            WHERE site_id = :site_id
              AND media_type = 'IMAGE'
              AND is_primary = TRUE
              AND is_active = TRUE
            LIMIT 1
        """),
        {"site_id": site["id"]},
    ).first()

    if existing:
        print("PRIMARY MEDIA ALREADY EXISTS")
        print("No database changes made.")
    else:
        destination = MEDIA_ROOT / STORAGE_KEY

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination.write_bytes(content)

        public_url = f"{BASE_URL}/{STORAGE_KEY}"
        now = datetime.utcnow()

        conn.execute(
            text("""
                INSERT INTO heritage_site_media (
                    id,
                    site_id,
                    media_type,
                    storage_key,
                    url,
                    title,
                    alt_text,
                    display_order,
                    is_primary,
                    is_active,
                    created_at,
                    updated_at
                )
                VALUES (
                    :id,
                    :site_id,
                    'IMAGE',
                    :storage_key,
                    :url,
                    :title,
                    :alt_text,
                    0,
                    TRUE,
                    TRUE,
                    :created_at,
                    :updated_at
                )
            """),
            {
                "id": str(uuid.uuid4()),
                "site_id": site["id"],
                "storage_key": STORAGE_KEY,
                "url": public_url,
                "title": site["name"],
                "alt_text": f"{site['name']} in {site['country']}",
                "created_at": now,
                "updated_at": now,
            },
        )

        print("MEDIA INSERTED SUCCESSFULLY")
        print("SITE :", site["name"])
        print("FILE :", destination)
        print("BYTES:", len(content))
        print("URL  :", public_url)
