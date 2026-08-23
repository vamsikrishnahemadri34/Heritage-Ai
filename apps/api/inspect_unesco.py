import json

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    data = json.load(f)

usable = [
    x for x in data
    if x.get("coordinates")
    and x.get("name_en")
    and x.get("states_names")
    and x.get("category") in ("Cultural", "Mixed")
]

print("USABLE CULTURAL/MIXED SITES:", len(usable))
print()

for i, x in enumerate(usable[:30], 1):
    print(
        f"{i}. {x['name_en']} | "
        f"{x['states_names']} | "
        f"{x['category']} | "
        f"{x['date_inscribed']} | "
        f"{x['coordinates']}"
    )
