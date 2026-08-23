import sys
import json
import re
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')

from sqlalchemy import create_engine, text
from app.core.config import settings


def normalize(value):
    value = value or ""
    value = unicodedata.normalize("NFKD", value)
    value = "".join(
        char for char in value
        if not unicodedata.combining(char)
    )
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


with open(
    "unesco_world_heritage.json",
    encoding="utf-8",
) as file:
    unesco = json.load(file)


engine = create_engine(settings.DATABASE_URL)

with engine.connect() as connection:
    sites = connection.execute(
        text("""
            SELECT id, name, slug
            FROM heritage_sites
            ORDER BY name
        """)
    ).fetchall()


unesco_records = [
    record
    for record in unesco
    if record.get("name_en")
]


by_normalized_name = {
    normalize(record["name_en"]): record
    for record in unesco_records
}


print("=" * 70)
print("HERITAGE SITE - UNESCO MATCH REPORT")
print("=" * 70)

exact_matches = 0
unmatched = []

for site in sites:
    db_name = site.name
    normalized = normalize(db_name)

    match = by_normalized_name.get(normalized)

    if match:
        exact_matches += 1

        print(
            f"[MATCH] {db_name}"
            f" => {match.get('name_en')}"
            f" | ID={match.get('id_no')}"
        )
    else:
        unmatched.append(site)

print()
print("=" * 70)
print(f"TOTAL DB SITES     : {len(sites)}")
print(f"EXACT MATCHES      : {exact_matches}")
print(f"UNMATCHED          : {len(unmatched)}")
print("=" * 70)

print()
print("UNMATCHED SITES")
print("=" * 70)

for site in unmatched:
    db_norm = normalize(site.name)

    candidates = []

    db_words = set(db_norm.split())

    for record in unesco_records:
        source_name = record.get("name_en", "")
        source_norm = normalize(source_name)
        source_words = set(source_norm.split())

        overlap = len(db_words & source_words)

        if overlap >= 2:
            candidates.append(
                (
                    overlap,
                    source_name,
                    record.get("id_no"),
                )
            )

    candidates.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    print()
    print(f"DB SITE: {site.name}")
    print(f"SLUG   : {site.slug}")

    if candidates:
        for overlap, name, id_no in candidates[:5]:
            print(
                f"  CANDIDATE: {name}"
                f" | ID={id_no}"
                f" | WORD OVERLAP={overlap}"
            )
    else:
        print("  NO NAME CANDIDATES")


print()
print("=" * 70)
print("REPORT COMPLETE — DATABASE WAS NOT MODIFIED")
print("=" * 70)




