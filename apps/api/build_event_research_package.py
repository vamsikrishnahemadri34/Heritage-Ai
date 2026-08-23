import json
from pathlib import Path

SRC = Path("full_remaining_80_unesco_enrichment.json")
OUT = Path("full_remaining_80_event_research_package.json")

data = json.loads(SRC.read_text(encoding="utf-8"))

if len(data["sites"]) != 80:
    raise ValueError(f"Expected 80 sites, got {len(data['sites'])}")

package = []

for site in data["sites"]:
    u = site["unesco"]

    package.append({
        "site_id": site["site_id"],
        "slug": site["slug"],
        "name": site["name"],
        "unesco_id": site["unesco_id"],
        "research_target": 4,
        "unesco_record": {
            "name": u.get("name_en"),
            "short_description": u.get("short_description_en"),
            "description": u.get("description_en"),
            "justification": u.get("justification_en"),
            "date_inscribed": u.get("date_inscribed"),
            "secondary_dates": u.get("secondary_dates"),
            "date_end": u.get("date_end"),
            "criteria": u.get("criteria_txt"),
            "category": u.get("category"),
            "states": u.get("states_names"),
            "region": u.get("region"),
            "components": u.get("components_list"),
        },
        "historical_events": []
    })

OUT.write_text(
    json.dumps(
        {
            "batch": "REMAINING_80",
            "target_sites": 80,
            "target_events": 320,
            "sites": package
        },
        ensure_ascii=False,
        indent=2
    ),
    encoding="utf-8"
)

print("=" * 80)
print("HERITAGEAI — EVENT RESEARCH PACKAGE")
print("=" * 80)
print("Sites          :", len(package))
print("Target events  :", sum(x["research_target"] for x in package))
print("Events present :", sum(len(x["historical_events"]) for x in package))
print("Database       : NOT MODIFIED")
print("File           :", OUT)
