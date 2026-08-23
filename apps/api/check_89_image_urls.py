import json

with open("heritage_89_candidates.json", encoding="utf-8") as f:
    candidates = json.load(f)

print("TOTAL CANDIDATES:", len(candidates))

missing = [
    x for x in candidates
    if not x.get("main_image_url")
]

print("MISSING IMAGE URLS:", len(missing))

for x in missing:
    print("-", x.get("name_en"))
