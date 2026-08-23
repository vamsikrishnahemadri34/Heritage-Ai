import json
from pathlib import Path

enrichment = json.loads(
    Path("full_remaining_80_unesco_enrichment.json")
    .read_text(encoding="utf-8")
)

sites = enrichment["sites"]

# Build candidate relationships using shared UNESCO region/category.
# No database changes.
relations = []

for site in sites:
    u = site["unesco"]

    candidates = []

    for target in sites:
        if target["slug"] == site["slug"]:
            continue

        tu = target["unesco"]

        score = 0

        if u.get("category") and u.get("category") == tu.get("category"):
            score += 2

        if u.get("region") and u.get("region") == tu.get("region"):
            score += 3

        states = set(u.get("states_names") or [])
        target_states = set(tu.get("states_names") or [])

        if states & target_states:
            score += 5

        if score > 0:
            candidates.append((score, target))

    candidates.sort(
        key=lambda x: (-x[0], x[1]["name"])
    )

    selected = candidates[:2]

    site_relations = []

    for order, (_, target) in enumerate(selected, 1):
        site_relations.append({
            "target_site_id": target["site_id"],
            "target_slug": target["slug"],
            "relation_type": "RELATED_TO",
            "description": (
                f"Related UNESCO World Heritage property in the "
                f"same geographic or cultural context as {site['name']}."
            ),
            "display_order": order,
        })

    relations.append({
        "site_id": site["site_id"],
        "slug": site["slug"],
        "name": site["name"],
        "relations": site_relations,
    })

Path("full_remaining_80_relations_preview.json").write_text(
    json.dumps(
        {
            "batch": "FULL_REMAINING_80",
            "sites": relations,
        },
        ensure_ascii=False,
        indent=2,
    ),
    encoding="utf-8",
)

print("=" * 80)
print("RELATIONS PREVIEW CREATED")
print("=" * 80)
print("Sites:", len(relations))
print(
    "Relations:",
    sum(len(x["relations"]) for x in relations)
)
print(
    "Sites with 2 relations:",
    sum(len(x["relations"]) == 2 for x in relations)
)
print(
    "Sites with <2 relations:",
    sum(len(x["relations"]) < 2 for x in relations)
)
print("Database modified: NO")
