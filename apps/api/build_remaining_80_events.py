import json
from pathlib import Path

SOURCE = Path("full_remaining_80_unesco_enrichment.json")
OUTPUT = Path("full_remaining_80_events.json")

data = json.loads(SOURCE.read_text(encoding="utf-8"))

sites = data["sites"]

if len(sites) != 80:
    raise ValueError(f"Expected 80 sites, found {len(sites)}")

# IMPORTANT:
# This builder only creates a structure/template.
# It does NOT invent historical facts.
# Historical event records must be supplied from verified research.

output = {
    "batch": "FULL_REMAINING_80",
    "sites": []
}

for site in sites:
    output["sites"].append({
        "site_id": site["site_id"],
        "slug": site["slug"],
        "name": site["name"],
        "historical_events": []
    })

OUTPUT.write_text(
    json.dumps(output, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print("=" * 80)
print("80-SITE EVENT WORKSPACE CREATED")
print("=" * 80)
print("Sites:", len(output["sites"]))
print("Events:", 0)
print("Database modified: NO")
print("File:", OUTPUT)
