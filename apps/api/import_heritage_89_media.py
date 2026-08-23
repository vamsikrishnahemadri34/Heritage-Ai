import json
import mimetypes
import uuid
from datetime import datetime
from pathlib import Path

import requests
from sqlalchemy import create_engine, text

from app.core.config import settings


CANDIDATES_FILE = Path("heritage_89_candidates.json")
MEDIA_ROOT = Path(settings.MEDIA_STORAGE_PATH)
BASE_URL = settings.MEDIA_BASE_URL.rstrip("/")

TIMEOUT = 30


def normalize_image_bytes(response: requests.Response) -> bytes:
    content_type = response.headers.get("content-type", "").lower()

    if response.status_code != 200:
        raise RuntimeError(f"HTTP {response.status_code}")

    if not content_type.startswith("image/"):
        raise RuntimeError(
            f"Expected image response, got {content_type or 'unknown content type'}"
        )

    content = response.content

    if not content:
        raise RuntimeError("Empty image response")

    return content


def main() -> None:
    print("=" * 40)
    print("HERITAGEAI 89-SITE MEDIA IMPORT")
    print("=" * 40)

    with open(CANDIDATES_FILE, encoding="utf-8") as f:
        candidates = json.load(f)

    print(f"Candidates : {len(candidates)}")

    engine = create_engine(settings.DATABASE_URL)

    inserted = 0
    skipped = 0
    failed = []

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "HeritageAI/1.0 "
                "(heritage research media importer)"
            )
        }
    )

    with engine.begin() as conn:

        for index, candidate in enumerate(candidates, 1):

            name = candidate["name"]
            slug = candidate["slug"]
            image_url = candidate["main_image_url"]

            print()
            print(f"[{index:02d}/89] {name}")

            site = conn.execute(
                text("""
                    SELECT id
                    FROM heritage_sites
                    WHERE slug = :slug
                    LIMIT 1
                """),
                {"slug": slug},
            ).mappings().first()

            if not site:
                failed.append(
                    {
                        "slug": slug,
                        "name": name,
                        "reason": "heritage site not found in database",
                    }
                )
                print("  FAILED: site not found")
                continue

            site_id = site["id"]

            existing = conn.execute(
                text("""
                    SELECT id, storage_key, url
                    FROM heritage_site_media
                    WHERE site_id = :site_id
                      AND media_type = 'IMAGE'
                      AND is_primary = TRUE
                      AND is_active = TRUE
                    LIMIT 1
                """),
                {"site_id": site_id},
            ).mappings().first()

            if existing:
                skipped += 1
                print("  SKIPPED: primary image already exists")
                continue

            try:
                response = session.get(
                    image_url,
                    timeout=TIMEOUT,
                    allow_redirects=True,
                )

                content = normalize_image_bytes(response)

                storage_key = (
                    f"heritage/{slug}/{slug}-primary.jpg"
                )

                storage_path = MEDIA_ROOT / storage_key

                storage_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                storage_path.write_bytes(content)

                public_url = (
                    f"{BASE_URL}/"
                    f"{storage_key}"
                )

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
                        "site_id": site_id,
                        "storage_key": storage_key,
                        "url": public_url,
                        "title": name,
                        "alt_text": (
                            f"{name} in "
                            f"{candidate.get('country', '')}"
                        ).strip(),
                        "created_at": now,
                        "updated_at": now,
                    },
                )

                inserted += 1

                print(
                    f"  INSERTED: "
                    f"{len(content):,} bytes"
                )

            except Exception as exc:
                failed.append(
                    {
                        "slug": slug,
                        "name": name,
                        "reason": str(exc),
                    }
                )

                print(f"  FAILED: {exc}")

    print()
    print("=" * 40)
    print("IMPORT SUMMARY")
    print("=" * 40)
    print(f"Candidates : {len(candidates)}")
    print(f"Inserted   : {inserted}")
    print(f"Skipped    : {skipped}")
    print(f"Failed     : {len(failed)}")

    if failed:
        print()
        print("FAILED SITES")
        print("============")

        for item in failed:
            print(
                f"- {item['name']} "
                f"| {item['reason']}"
            )

        with open(
            "heritage_media_import_failures.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                failed,
                f,
                ensure_ascii=False,
                indent=2,
            )

        print()
        print(
            "Failure report:"
            " heritage_media_import_failures.json"
        )

    print()
    print("Import process completed.")


if __name__ == "__main__":
    main()
