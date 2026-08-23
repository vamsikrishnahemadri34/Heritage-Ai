from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:

    rows = conn.execute(
        text("""
            SELECT
                hs.name,
                hsm.id,
                hsm.site_id,
                hsm.media_type,
                hsm.storage_key,
                hsm.url,
                hsm.title,
                hsm.alt_text,
                hsm.display_order,
                hsm.is_primary,
                hsm.is_active
            FROM heritage_site_media hsm
            JOIN heritage_sites hs
                ON hs.id = hsm.site_id
            ORDER BY hs.name
            LIMIT 15
        """)
    ).fetchall()

    print("EXISTING HERITAGE MEDIA")
    print("======================")

    for row in rows:
        print()
        print("SITE         :", row.name)
        print("ID           :", row.id)
        print("SITE ID      :", row.site_id)
        print("MEDIA TYPE   :", row.media_type)
        print("STORAGE KEY  :", row.storage_key)
        print("URL          :", row.url)
        print("TITLE        :", row.title)
        print("ALT TEXT     :", row.alt_text)
        print("DISPLAY ORDER:", row.display_order)
        print("PRIMARY      :", row.is_primary)
        print("ACTIVE       :", row.is_active)
