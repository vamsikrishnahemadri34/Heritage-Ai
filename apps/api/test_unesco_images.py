import json
import requests

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    data = json.load(f)

usable = [
    x for x in data
    if x.get("coordinates")
    and x.get("name_en")
    and x.get("states_names")
    and x.get("category") in ("Cultural", "Mixed")
]

print("TESTING UNESCO IMAGE URLS")
print("=========================")

tested = 0

for site in usable:
    url = site.get("main_image_url")

    if not url:
        continue

    try:
        r = requests.get(
            url,
            timeout=15,
            allow_redirects=True,
            stream=True,
            headers={"User-Agent": "HeritageAI/1.0"},
        )

        content_type = r.headers.get("content-type", "")

        print()
        print("SITE :", site["name_en"])
        print("URL  :", url)
        print("HTTP :", r.status_code)
        print("TYPE :", content_type)

        r.close()

    except Exception as e:
        print()
        print("SITE :", site["name_en"])
        print("ERROR:", str(e))

    tested += 1

    if tested >= 5:
        break
