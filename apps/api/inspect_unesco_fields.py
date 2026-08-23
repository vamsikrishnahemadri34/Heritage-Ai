import json
from pathlib import Path

audit = json.loads(
    Path("full_remaining_80_matches.json").read_text(encoding="utf-8")
) if Path("full_remaining_80_matches.json").exists() else json.loads(
    Path("full_remaining_unesco_matches.json").read_text(encoding="utf-8")
)

ids = {str(x["unesco_id"]) for x in audit["matched"]}

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    records = json.load(f)

matched = [
    r for r in records
    if str(r.get("id_no")) in ids
]

print("=" * 80)
print("UNESCO SOURCE FIELD AUDIT")
print("=" * 80)
print("Records:", len(matched))
print()

if matched:
    print("AVAILABLE FIELDS:")
    for key in matched[0].keys():
        print("-", key)

print()
print("SAMPLE RECORD:")
print("=" * 80)
print(json.dumps(matched[0], ensure_ascii=False, indent=2))
