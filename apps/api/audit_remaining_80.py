import json
from sqlalchemy import create_engine, text
from app.core.config import settings

UNESCO_FILE = "unesco_world_heritage.json"

engine = create_engine(settings.DATABASE_URL)

with open(UNESCO_FILE, encoding="utf-8") as f:
    unesco = json.load(f)

with engine.connect() as db:

    rows = db.execute(text("""
        SELECT
            hs.id,
            hs.name,
            hs.slug,
            hs.description,
            hs.significance,
            hs.established_year,
            hs.category
        FROM heritage_sites hs
        WHERE NOT EXISTS (
            SELECT 1
            FROM heritage_site_historical_events e
            WHERE e.site_id = hs.id
        )
        ORDER BY hs.name
    """)).mappings().all()

print("=" * 80)
print("HERITAGEAI - FULL REMAINING SITE AUDIT")
print("=" * 80)
print("REMAINING SITES:", len(rows))
print()

matched = []
unmatched = []

for site in rows:

    name = (site["name"] or "").strip().lower()

    candidates = []

    for record in unesco:

        source_name = (record.get("name_en") or "").strip().lower()

        if not source_name:
            continue

        if name == source_name:
            candidates.append(record)
        elif name in source_name or source_name in name:
            candidates.append(record)

    if candidates:

        # Prefer the closest name.
        candidates.sort(
            key=lambda r: abs(
                len((r.get("name_en") or ""))
                - len(site["name"] or "")
            )
        )

        record = candidates[0]

        matched.append({
            "id": site["id"],
            "name": site["name"],
            "slug": site["slug"],
            "unesco_id": record.get("id_no"),
            "unesco_name": record.get("name_en"),
            "date_inscribed": record.get("date_inscribed"),
            "category": record.get("category"),
        })

    else:
        unmatched.append({
            "id": site["id"],
            "name": site["name"],
            "slug": site["slug"],
        })

print("UNESCO MATCHED  :", len(matched))
print("UNESCO UNMATCHED:", len(unmatched))
print()

print("=" * 80)
print("UNMATCHED SITES")
print("=" * 80)

for site in unmatched:
    print(
        f'{site["name"]} | '
        f'{site["slug"]} | '
        f'ID={site["id"]}'
    )

with open(
    "full_remaining_unesco_matches.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        {
            "remaining_sites": len(rows),
            "matched": matched,
            "unmatched": unmatched,
        },
        f,
        ensure_ascii=False,
        indent=2,
    )

print()
print("AUDIT FILE CREATED:")
print("full_remaining_unesco_matches.json")

