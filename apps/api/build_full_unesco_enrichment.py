import json
from pathlib import Path

audit = json.loads(
    Path("full_remaining_unesco_matches.json").read_text(encoding="utf-8")
)

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    unesco = json.load(f)

by_id = {
    str(r.get("id_no")): r
    for r in unesco
}

sites = []

for item in audit["matched"]:
    record = by_id.get(str(item["unesco_id"]))

    if record is None:
        raise ValueError(
            f"Missing UNESCO record: {item['unesco_id']} | {item['name']}"
        )

    sites.append({
        "site_id": item["id"],
        "slug": item["slug"],
        "name": item["name"],
        "unesco_id": item["unesco_id"],
        "unesco": {
            "name_en": record.get("name_en"),
            "short_description_en": record.get("short_description_en"),
            "description_en": record.get("description_en"),
            "justification_en": record.get("justification_en"),
            "date_inscribed": record.get("date_inscribed"),
            "secondary_dates": record.get("secondary_dates"),
            "danger": record.get("danger"),
            "danger_list": record.get("danger_list"),
            "area_hectares": record.get("area_hectares"),
            "cultural_criteria": record.get("cultural_criteria"),
            "natural_criteria": record.get("natural_criteria"),
            "criteria_txt": record.get("criteria_txt"),
            "category": record.get("category"),
            "states_names": record.get("states_names"),
            "region": record.get("region"),
            "transboundary": record.get("transboundary"),
            "coordinates": record.get("coordinates"),
            "main_image_url": record.get("main_image_url"),
            "main_image_author": record.get("main_image_author"),
            "main_image_copyright": record.get("main_image_copyright"),
            "main_image_caption_en": record.get("main_image_caption_en"),
            "images_urls": record.get("images_urls"),
            "uuid": record.get("uuid"),
            "main_video_url": record.get("main_video_url"),
            "main_video_author": record.get("main_video_author"),
            "main_video_caption_en": record.get("main_video_caption_en"),
            "components_list": record.get("components_list"),
            "components_count": record.get("components_count"),
        }
    })

# Add the separately verified Auschwitz record.
auschwitz = next(
    x for x in audit["unmatched"]
    if x["slug"].startswith("auschwitz-birkenau")
)

record = by_id.get("31")

if record is None:
    raise ValueError("UNESCO ID 31 not found for Auschwitz")

sites.append({
    "site_id": auschwitz["id"],
    "slug": auschwitz["slug"],
    "name": auschwitz["name"],
    "unesco_id": "31",
    "unesco": {
        "name_en": record.get("name_en"),
        "short_description_en": record.get("short_description_en"),
        "description_en": record.get("description_en"),
        "justification_en": record.get("justification_en"),
        "date_inscribed": record.get("date_inscribed"),
        "secondary_dates": record.get("secondary_dates"),
        "danger": record.get("danger"),
        "danger_list": record.get("danger_list"),
        "area_hectares": record.get("area_hectares"),
        "cultural_criteria": record.get("cultural_criteria"),
        "natural_criteria": record.get("natural_criteria"),
        "criteria_txt": record.get("criteria_txt"),
        "category": record.get("category"),
        "states_names": record.get("states_names"),
        "region": record.get("region"),
        "transboundary": record.get("transboundary"),
        "coordinates": record.get("coordinates"),
        "main_image_url": record.get("main_image_url"),
        "main_image_author": record.get("main_image_author"),
        "main_image_copyright": record.get("main_image_copyright"),
        "main_image_caption_en": record.get("main_image_caption_en"),
        "images_urls": record.get("images_urls"),
        "uuid": record.get("uuid"),
        "main_video_url": record.get("main_video_url"),
        "main_video_author": record.get("main_video_author"),
        "main_video_caption_en": record.get("main_video_caption_en"),
        "components_list": record.get("components_list"),
        "components_count": record.get("components_count"),
    }
})

if len(sites) != 80:
    raise ValueError(f"Expected 80 sites, got {len(sites)}")

Path("full_remaining_80_unesco_enrichment.json").write_text(
    json.dumps(
        {
            "batch": "FULL_REMAINING_80",
            "source": "UNESCO_WORLD_HERITAGE_DATASET",
            "sites": sites,
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

print("=" * 80)
print("FULL UNESCO ENRICHMENT CREATED")
print("=" * 80)
print("Sites:", len(sites))
print("Source: UNESCO dataset")
print("Database modified: NO")
print("File: full_remaining_80_unesco_enrichment.json")
