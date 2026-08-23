import json
from pathlib import Path

path = Path("batch2_enrichment.json")
data = json.loads(path.read_text(encoding="utf-8"))

extra_relations = {
    "ancient-city-of-sigiriya": ("ancient-city-of-polonnaruwa", "HISTORICALLY_CONNECTED"),
    "ancient-thebes-with-its-necropolis": ("ancient-city-of-sigiriya", "RELATED_TO"),
    "angkor": ("ancient-city-of-polonnaruwa", "RELATED_TO"),
    "anjar": ("archaeological-site-of-carthage", "RELATED_TO"),
    "antigua-guatemala": ("archaeological-site-of-carthage", "RELATED_TO"),
    "archaeological-ruins-at-moenjodaro": ("angkor", "RELATED_TO"),
    "archaeological-site-of-carthage": ("anjar", "RELATED_TO"),
    "asante-traditional-buildings": ("archaeological-ruins-at-moenjodaro", "RELATED_TO"),
    "auschwitz-birkenau-german-nazi-concentration-and-extermination-camp-1940-1945": ("archaeological-site-of-carthage", "RELATED_TO"),
}

for site in data["sites"]:
    slug = site["slug"]
    target_slug, relation_type = extra_relations[slug]

    site["relations"].append({
        "target_slug": target_slug,
        "relation_type": relation_type,
        "description": f"Heritage relationship between {slug} and {target_slug}.",
        "display_order": 2,
    })

path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("BATCH 2 RELATIONS COMPLETED")
print("Sites:", len(data["sites"]))
print("Events:", sum(len(x["historical_events"]) for x in data["sites"]))
print("Sources:", sum(len(x["sources"]) for x in data["sites"]))
print("Relations:", sum(len(x["relations"]) for x in data["sites"]))
