import json
import re
from collections import Counter

DATA_FILE = "unesco_world_heritage.json"
OUTPUT_FILE = "heritage_89_candidates.json"

EXISTING_SLUGS = {
    "acropolis-of-athens",
    "ajanta-caves",
    "angkor-wat",
    "brihadeeswarar-temple",
    "ellora-caves",
    "hampi",
    "konark-sun-temple",
    "machu-picchu",
    "petra",
    "red-fort",
    "taj-mahal",
}

def slugify(value):
    value = re.sub(r"<[^>]+>", "", value or "")
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")

with open(DATA_FILE, encoding="utf-8") as f:
    data = json.load(f)

usable = []

for item in data:
    coords = item.get("coordinates")

    if (
        item.get("name_en")
        and item.get("states_names")
        and item.get("category") in ("Cultural", "Mixed")
        and coords
        and coords.get("lat") is not None
        and coords.get("lon") is not None
    ):
        slug = slugify(item["name_en"])

        if slug not in EXISTING_SLUGS:
            usable.append(item)

REGIONS = {
    "India / South Asia": (
        15,
        {
            "India",
            "Pakistan",
            "Bangladesh",
            "Nepal",
            "Sri Lanka",
            "Bhutan",
            "Afghanistan",
            "Maldives",
        },
    ),

    "East & Southeast Asia": (
        15,
        {
            "China",
            "Japan",
            "Republic of Korea",
            "Democratic People's Republic of Korea",
            "Mongolia",
            "Thailand",
            "Cambodia",
            "Viet Nam",
            "Lao People's Democratic Republic",
            "Malaysia",
            "Indonesia",
            "Philippines",
            "Singapore",
            "Myanmar",
            "Brunei Darussalam",
            "Timor-Leste",
        },
    ),

    "Europe": (
        20,
        {
            "Italy",
            "Germany",
            "France",
            "Spain",
            "United Kingdom of Great Britain and Northern Ireland",
            "Greece",
            "Czechia",
            "Portugal",
            "Poland",
            "Belgium",
            "Sweden",
            "Netherlands (Kingdom of the)",
            "Austria",
            "Romania",
            "Switzerland",
            "Denmark",
            "Croatia",
            "Norway",
            "Hungary",
            "Bulgaria",
            "Finland",
            "Ukraine",
            "Slovakia",
            "Lithuania",
            "Serbia",
            "Slovenia",
            "Montenegro",
            "Bosnia and Herzegovina",
            "Albania",
            "Cyprus",
            "Malta",
            "Latvia",
            "Estonia",
            "Ireland",
            "Iceland",
            "Luxembourg",
            "North Macedonia",
            "San Marino",
            "Andorra",
            "Belarus",
            "Republic of Moldova",
        },
    ),

    "Middle East / Central Asia": (
        10,
        {
            "Iran (Islamic Republic of)",
            "Iraq",
            "Jordan",
            "Lebanon",
            "Israel",
            "State of Palestine",
            "Saudi Arabia",
            "Oman",
            "United Arab Emirates",
            "Qatar",
            "Bahrain",
            "Kuwait",
            "Uzbekistan",
            "Kazakhstan",
            "Kyrgyzstan",
            "Tajikistan",
            "Turkmenistan",
            "Azerbaijan",
            "Armenia",
            "Georgia",
            "Syrian Arab Republic",
            "Yemen",
        },
    ),

    "Africa": (
        10,
        {
            "Egypt",
            "Ethiopia",
            "Kenya",
            "United Republic of Tanzania",
            "Uganda",
            "South Africa",
            "Zimbabwe",
            "Zambia",
            "Botswana",
            "Namibia",
            "Ghana",
            "Nigeria",
            "Senegal",
            "Mali",
            "Niger",
            "Morocco",
            "Algeria",
            "Tunisia",
            "Libya",
            "Cameroon",
            "Benin",
            "Togo",
            "Gambia",
            "Guinea",
            "Guinea-Bissau",
            "Côte d'Ivoire",
            "Madagascar",
            "Mauritius",
            "Mozambique",
            "Malawi",
            "Burkina Faso",
        },
    ),

    "Americas / Caribbean": (
        9,
        {
            "United States of America",
            "Canada",
            "Mexico",
            "Guatemala",
            "Belize",
            "Honduras",
            "El Salvador",
            "Nicaragua",
            "Costa Rica",
            "Panama",
            "Cuba",
            "Jamaica",
            "Dominican Republic",
            "Haiti",
            "Colombia",
            "Venezuela (Bolivarian Republic of)",
            "Ecuador",
            "Peru",
            "Bolivia (Plurinational State of)",
            "Chile",
            "Argentina",
            "Brazil",
            "Uruguay",
            "Paraguay",
            "Suriname",
            "Guyana",
        },
    ),
}

selected = []
selected_ids = set()

def add_site(item, region):
    identifier = (
        item.get("id_no")
        or item.get("uuid")
        or item.get("name_en")
    )

    if identifier in selected_ids:
        return False

    selected.append(
        {
            "group": region,
            "name": item["name_en"],
            "slug": slugify(item["name_en"]),
            "country": (item.get("states_names") or [""])[0],
            "category": item.get("category"),
            "date_inscribed": item.get("date_inscribed"),
            "latitude": item["coordinates"]["lat"],
            "longitude": item["coordinates"]["lon"],
            "description": item.get("short_description_en"),
            "unesco_id": item.get("id_no"),
            "unesco_uuid": item.get("uuid"),
            "main_image_url": item.get("main_image_url"),
        }
    )

    selected_ids.add(identifier)
    return True

for region, (quota, countries) in REGIONS.items():

    candidates = [
        item
        for item in usable
        if set(item.get("states_names") or []) & countries
    ]

    candidates.sort(
        key=lambda x: (
            int(x.get("date_inscribed") or 9999),
            x.get("name_en", ""),
        )
    )

    added = 0

    for item in candidates:
        if add_site(item, region):
            added += 1

        if added >= quota:
            break

# Safety fallback to guarantee exactly 89.
if len(selected) < 89:

    remaining = [
        item
        for item in usable
        if (
            item.get("id_no") or
            item.get("uuid") or
            item.get("name_en")
        ) not in selected_ids
    ]

    remaining.sort(
        key=lambda x: (
            int(x.get("date_inscribed") or 9999),
            x.get("name_en", ""),
        )
    )

    for item in remaining:
        if len(selected) >= 89:
            break

        add_site(item, "Global Fallback")

if len(selected) != 89:
    raise RuntimeError(
        f"Expected 89 candidates but generated {len(selected)}"
    )

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(selected, f, ensure_ascii=False, indent=2)

print("========================================")
print("HERITAGEAI 89-SITE CANDIDATE PREVIEW")
print("========================================")
print()

counts = Counter(x["group"] for x in selected)

for region, count in counts.items():
    print(f"{region}: {count}")

print()
print("TOTAL SELECTED:", len(selected))
print("OUTPUT:", OUTPUT_FILE)
print()
print("DATABASE WAS NOT MODIFIED.")
