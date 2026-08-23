import json

with open("heritage_89_candidates.json", encoding="utf-8") as f:
    candidates = json.load(f)

for i, x in enumerate(candidates, 1):
    if not x.get("main_image_url"):
        print("MISSING IMAGE CANDIDATE")
        print("======================")
        print("INDEX       :", i)
        print("NAME        :", x.get("name_en"))
        print("COUNTRY     :", x.get("country") or x.get("states_names"))
        print("CATEGORY    :", x.get("category"))
        print("COORDINATES :", x.get("coordinates"))
        print("ALL KEYS    :", list(x.keys()))
        print("FULL RECORD :", x)
