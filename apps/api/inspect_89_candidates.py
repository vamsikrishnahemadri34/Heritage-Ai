import json

with open("heritage_89_candidates.json", encoding="utf-8") as f:
    sites = json.load(f)

for i, site in enumerate(sites, 1):
    print(
        f"{i:03d}. "
        f"[{site['group']}] "
        f"{site['name']} | "
        f"{site['country']} | "
        f"{site['category']} | "
        f"{site['date_inscribed']} | "
        f"{site['latitude']}, {site['longitude']}"
    )
