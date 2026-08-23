from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as db:
    rows = db.execute(text("""
        SELECT
            hs.name,
            hs.slug,
            COUNT(DISTINCT CASE
                WHEN m.media_type = 'IMAGE' AND m.is_active = 1
                THEN m.id END) AS images,
            COUNT(DISTINCT CASE
                WHEN m.media_type = 'VIDEO' AND m.is_active = 1
                THEN m.id END) AS videos,
            COUNT(DISTINCT CASE
                WHEN src.is_active = 1
                THEN src.id END) AS sources
        FROM heritage_sites hs
        LEFT JOIN heritage_site_media m
            ON m.site_id = hs.id
        LEFT JOIN heritage_site_sources src
            ON src.site_id = hs.id
        WHERE NOT EXISTS (
            SELECT 1
            FROM heritage_site_historical_events e
            WHERE e.site_id = hs.id
        )
        GROUP BY hs.id, hs.name, hs.slug
        ORDER BY hs.name
    """)).mappings().all()

print("=" * 80)
print("REMAINING 80 MEDIA/SOURCE AUDIT")
print("=" * 80)

print("SITES:", len(rows))
print()

for r in rows:
    print(
        f'{r["name"]} | '
        f'images={r["images"]} | '
        f'videos={r["videos"]} | '
        f'sources={r["sources"]}'
    )
