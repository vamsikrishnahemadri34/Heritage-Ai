import json
from collections import Counter

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    data = json.load(f)

usable = [
    x for x in data
    if x.get("coordinates")
    and x.get("name_en")
    and x.get("states_names")
    and x.get("category") in ("Cultural", "Mixed")
]

countries = Counter()

for item in usable:
    for country in item.get("states_names") or []:
        countries[country] += 1

print("TOP COUNTRIES WITH USABLE CULTURAL/MIXED SITES")
print("==============================================")

for country, count in countries.most_common(100):
    print(f"{country}: {count}")
