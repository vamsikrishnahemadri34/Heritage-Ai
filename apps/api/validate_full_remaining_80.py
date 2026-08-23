import json
from pathlib import Path

unesco = json.loads(
    Path("full_remaining_80_unesco_enrichment.json")
    .read_text(encoding="utf-8")
)

sm = json.loads(
    Path("full_remaining_80_sources_media_preview.json")
    .read_text(encoding="utf-8")
)

relations = json.loads(
    Path("full_remaining_80_relations_preview.json")
    .read_text(encoding="utf-8")
)

u = {x["slug"]: x for x in unesco["sites"]}
s = {x["slug"]: x for x in sm["sites"]}
r = {x["slug"]: x for x in relations["sites"]}

errors = []

if len(u) != 80:
    errors.append(f"UNESCO sites={len(u)}")

if len(s) != 80:
    errors.append(f"source/media sites={len(s)}")

if len(r) != 80:
    errors.append(f"relation sites={len(r)}")

if set(u) != set(s):
    errors.append("UNESCO/source site sets differ")

if set(u) != set(r):
    errors.append("UNESCO/relation site sets differ")

if len(set(u)) != 80:
    errors.append("duplicate UNESCO slugs")

unesco_ids = [x["unesco_id"] for x in unesco["sites"]]

if len(set(unesco_ids)) != 80:
    errors.append("duplicate UNESCO IDs")

source_count = sum(len(x["sources"]) for x in s.values())
video_count = sum(len(x["media"]) for x in s.values())
relation_count = sum(len(x["relations"]) for x in r.values())

if source_count != 80:
    errors.append(f"sources={source_count}")

if relation_count != 160:
    errors.append(f"relations={relation_count}")

for slug, site in r.items():

    if len(site["relations"]) != 2:
        errors.append(f"{slug}: relation count != 2")

    for relation in site["relations"]:
        if relation["target_slug"] not in u:
            errors.append(
                f"{slug}: invalid target {relation['target_slug']}"
            )

for slug, site in s.items():

    if len(site["sources"]) != 1:
        errors.append(f"{slug}: source count != 1")

    for media in site["media"]:
        if media["media_type"] != "VIDEO":
            errors.append(
                f"{slug}: invalid media type {media['media_type']}"
            )

print("=" * 80)
print("HERITAGEAI — FULL PRE-IMPORT VALIDATION")
print("=" * 80)

print("UNESCO SITES :", len(u))
print("SOURCES      :", source_count)
print("VIDEOS       :", video_count)
print("RELATIONS    :", relation_count)

if errors:
    print()
    print("VALIDATION: FAIL")
    print()
    for error in errors:
        print("ERROR:", error)
    raise SystemExit(1)

print()
print("VALIDATION: PASS")
print("DATABASE MODIFIED: NO")

