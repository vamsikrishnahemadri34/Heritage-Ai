import uuid
from datetime import datetime
from pathlib import Path

import requests
from sqlalchemy import create_engine, text

from app.core.config import settings


SITE_SLUG = "buddhist-ruins-of-takht-i-bahi-and-neighbouring-city-remains-at-sahr-i-bahlol"

IMAGE_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/2/21/"
    "Takht-i-Bahi_Buddhist_Monastery.jpg"
)

MEDIA_ROOT = Path(settings.MEDIA_STORAGE_PATH)
BASE_URL = settings.MEDIA_BASE_URL.rstrip("/")


def main() -> None:
    print("=" * 50)
    print("TAKHT-I-BAHI MEDIA PATCH")
    print("=" * 50)

    engine = create_engine(settings.DATABASE_URL)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "HeritageAI/1.0 "
                "(heritage research media importer)"
            )
        }
    )

    response = session.get(
        IMAGE_URL,
        timeout=30,
        allow_redirects=True,
    )

    print("HTTP:", response.status_code)
    print("CONTENT-TYPE:", response.headers.get("content-type"))

    if response.status_code != 200:
        raise RuntimeError(
            f"Image download failed: HTTP {response.status_code}"
        )

    content_type = response.headers.get("content-type", "").lower()

    if not content_type.startswith("image/"):
        raise RuntimeError(
            f"Expected image response, got {content_type}"
        )

    content = response.content

    if not content:
        raise RuntimeError("Downloaded image is empty.")

    with engine.begin() as conn:
        site = conn.execute(
            text("""
                SELECT id, name, country
                FROM heritage_sites
                WHERE slug = :slug
                LIMIT 1
            """),
            {"slug": SITE_SLUG},
        ).mappings().first()

        if not site:
            raise RuntimeError(
                f"Heritage site not found: {SITE_SLUG}"
            )

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
            print("No database changes required.")
            return

        storage_key = (
            f"heritage/{SITE_SLUG}/{SITE_SLUG}-primary.jpg"
        )

        storage_path = MEDIA_ROOT / storage_key

        storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        storage_path.write_bytes(content)

        public_url = f"{BASE_URL}/{storage_key}"

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
                "storage_key": storage_key,
                "url": public_url,
                "title": site["name"],
                "alt_text": (
                    f"{site['name']} in {site['country']}"
                ),
                "created_at": now,
                "updated_at": now,
            },
        )

        print()
        print("PATCH SUCCESSFUL")
        print("SITE:", site["name"])
        print("BYTES:", f"{len(content):,}")
        print("STORAGE KEY:", storage_key)
        print("URL:", public_url)


if __name__ == "__main__":
    main()

