import json

path = "heritage_89_candidates.json"

with open(path, encoding="utf-8") as f:
    candidates = json.load(f)

target = "buddhist-ruins-of-takht-i-bahi-and-neighbouring-city-remains-at-sahr-i-bahlol"

image_url = "https://upload.wikimedia.org/wikipedia/commons/2/21/Takht-i-Bahi_Buddhist_Monastery.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=original"

updated = False

for site in candidates:
    if site.get("slug") == target:
        site["main_image_url"] = image_url
        updated = True
        print("UPDATED:", site["name"])

if not updated:
    raise RuntimeError("Target site was not found.")

with open(path, "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)

print("Candidate file updated successfully.")
