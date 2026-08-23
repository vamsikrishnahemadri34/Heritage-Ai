import json
from pathlib import Path

enrichment = json.loads(
    Path("full_remaining_80_unesco_enrichment.json")
    .read_text(encoding="utf-8")
)

preview = []

for site in enrichment["sites"]:

    u = site["unesco"]

    sources = [{
        "source_type": "UNESCO",
        "title": f"UNESCO World Heritage Centre — {site['name']}",
        "organization": "UNESCO World Heritage Centre",
        "url": f"https://whc.unesco.org/en/list/{site['unesco_id']}/",
        "citation_text": (
            f"UNESCO World Heritage Centre. "
            f"{site['name']}. World Heritage List, "
            f"inscribed {u.get('date_inscribed')}."
        ),
        "language": "en",
        "display_order": 1,
        "is_verified": True,
        "is_active": True,
    }]

    media = []

    if u.get("main_video_url"):
        media.append({
            "media_type": "VIDEO",
            "url": u["main_video_url"],
            "storage_key": u["main_video_url"],
            "title": u.get("main_video_caption_en")
                     or f"{site['name']} — UNESCO",
            "alt_text": f"UNESCO video for {site['name']}",
            "display_order": 1,
            "is_primary": False,
            "is_active": True,
        })

    preview.append({
        "site_id": site["site_id"],
        "slug": site["slug"],
        "name": site["name"],
        "sources": sources,
        "media": media,
    })

Path("full_remaining_80_sources_media_preview.json").write_text(
    json.dumps(
        {
            "batch": "FULL_REMAINING_80",
            "sites": preview,
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

print("=" * 80)
print("SOURCES + MEDIA PREVIEW CREATED")
print("=" * 80)
print("Sites:", len(preview))
print(
    "Sources:",
    sum(len(x["sources"]) for x in preview)
)
print(
    "Videos:",
    sum(len(x["media"]) for x in preview)
)
print("Existing images: PRESERVED")
print("Database modified: NO")
