from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:

    rows = conn.execute(
        text("""
            SELECT
                hs.id,
                hs.name,
                hs.slug,

                (
                    SELECT COUNT(*)
                    FROM heritage_site_historical_events e
                    WHERE e.site_id = hs.id
                      AND e.is_active = 1
                ) AS event_count,

                (
                    SELECT COUNT(*)
                    FROM heritage_site_sources s
                    WHERE s.site_id = hs.id
                      AND s.is_active = 1
                ) AS source_count,

                (
                    SELECT COUNT(*)
                    FROM heritage_site_relations r
                    WHERE r.source_site_id = hs.id
                      AND r.is_active = 1
                ) AS relation_count,

                (
                    SELECT COUNT(*)
                    FROM heritage_site_media m
                    WHERE m.site_id = hs.id
                      AND m.is_active = 1
                ) AS media_count

            FROM heritage_sites hs
            WHERE hs.is_active = 1
            ORDER BY hs.name
        """)
    ).fetchall()

print("=" * 100)
print("HERITAGEAI - ENRICHMENT GAP REPORT")
print("=" * 100)

print(
    f"{'SITE':55} "
    f"{'EVENTS':>7} "
    f"{'SOURCES':>8} "
    f"{'RELATIONS':>10} "
    f"{'MEDIA':>7} "
    f"STATUS"
)

print("-" * 100)

for row in rows:

    complete = (
        row.event_count > 0
        and row.source_count > 0
    )

    status = "COMPLETE" if complete else "NEEDS ENRICHMENT"

    print(
        f"{row.name[:55]:55} "
        f"{row.event_count:7} "
        f"{row.source_count:8} "
        f"{row.relation_count:10} "
        f"{row.media_count:7} "
        f"{status}"
    )

print("-" * 100)

print(f"TOTAL ACTIVE SITES : {len(rows)}")

print(
    "SITES WITH EVENTS  : "
    f"{sum(r.event_count > 0 for r in rows)}"
)

print(
    "SITES WITH SOURCES : "
    f"{sum(r.source_count > 0 for r in rows)}"
)

print(
    "SITES WITH MEDIA   : "
    f"{sum(r.media_count > 0 for r in rows)}"
)

print(
    "SITES NEEDING WORK : "
    f"{sum(not (r.event_count > 0 and r.source_count > 0) for r in rows)}"
)

print("=" * 100)
print("DATABASE WAS NOT MODIFIED")
print("=" * 100)
