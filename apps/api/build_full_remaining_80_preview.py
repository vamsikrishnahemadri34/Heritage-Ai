import json
from pathlib import Path

audit = json.loads(
    Path("full_remaining_unesco_matches.json")
    .read_text(encoding="utf-8")
)

sites = audit["matched"]

# Auschwitz was unmatched because of HTML formatting in the UNESCO name.
# Its canonical UNESCO ID was already verified as 31.
unmatched = audit["unmatched"]

if len(sites) != 79 or len(unmatched) != 1:
    raise ValueError(
        f"Expected 79 matched + 1 unmatched, got "
        f"{len(sites)} matched + {len(unmatched)} unmatched"
    )

auschwitz = unmatched[0]

sites.append({
    "id": auschwitz["id"],
    "name": auschwitz["name"],
    "slug": auschwitz["slug"],
    "unesco_id": "31",
    "unesco_name": (
        "Auschwitz Birkenau <br /><small>"
        "German Nazi Concentration and Extermination Camp "
        "(1940-1945)</small>"
    ),
    "date_inscribed": "1979",
    "category": "Cultural",
})

if len(sites) != 80:
    raise ValueError("Final site count is not 80")

preview = {
    "batch": "FULL_REMAINING_80",
    "sites": []
}

for site in sites:

    slug = site["slug"]

    preview["sites"].append({
        "site_id": site["id"],
        "slug": slug,
        "name": site["name"],
        "unesco_id": site["unesco_id"],
        "unesco_name": site["unesco_name"],
        "date_inscribed": site["date_inscribed"],
        "category": site["category"],
        "historical_events": [],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": f"UNESCO World Heritage Centre — {site['name']}",
                "organization": "UNESCO World Heritage Centre",
                "url": "https://whc.unesco.org/",
                "language": "en",
                "display_order": 1,
            },
            {
                "source_type": "WEBSITE",
                "title": f"Heritage reference — {site['name']}",
                "organization": "HeritageAI",
                "url": None,
                "language": "en",
                "display_order": 2,
            }
        ],
        "relations": []
    })

Path("full_remaining_80_preview.json").write_text(
    json.dumps(preview, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("=" * 70)
print("FULL REMAINING 80 PREVIEW CREATED")
print("=" * 70)
print("Sites   :", len(preview["sites"]))
print("Sources :", sum(len(s["sources"]) for s in preview["sites"]))
print("Events  :", sum(len(s["historical_events"]) for s in preview["sites"]))
print("Relations:", sum(len(s["relations"]) for s in preview["sites"]))
print()
print("DATABASE MODIFIED: NO")
print("FILE: full_remaining_80_preview.json")
