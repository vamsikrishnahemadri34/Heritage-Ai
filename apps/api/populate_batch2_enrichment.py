import json
from pathlib import Path

PATH = Path("batch2_enrichment.json")

sites = [
    "ancient-city-of-sigiriya",
    "ancient-thebes-with-its-necropolis",
    "angkor",
    "anjar",
    "antigua-guatemala",
    "archaeological-ruins-at-moenjodaro",
    "archaeological-site-of-carthage",
    "asante-traditional-buildings",
    "auschwitz-birkenau-german-nazi-concentration-and-extermination-camp-1940-1945",
]

events = {
    "ancient-city-of-sigiriya": [
        ("Royal citadel established", "Construction of the royal citadel and palace complex at Sigiriya.", 477, "YEAR"),
        ("Sigiriya becomes royal capital", "King Kashyapa established Sigiriya as his royal capital.", 477, "YEAR"),
        ("Royal occupation ends", "The royal court moved away from Sigiriya after the fall of Kashyapa.", 495, "YEAR"),
        ("Buddhist monastic occupation", "Sigiriya continued as a Buddhist monastery after its royal period.", 600, "APPROXIMATE"),
    ],
    "ancient-thebes-with-its-necropolis": [
        ("Thebes becomes major Egyptian centre", "Thebes developed into one of ancient Egypt's most important religious and political centres.", -2000, "APPROXIMATE"),
        ("Temple development at Karnak", "Major monumental development transformed the Karnak temple complex.", -1500, "APPROXIMATE"),
        ("Valley of the Kings developed", "The western Theban necropolis became a major royal burial area.", -1500, "APPROXIMATE"),
        ("Theban monuments continue", "The temples and necropolis remained important religious and funerary monuments.", -1000, "APPROXIMATE"),
    ],
    "angkor": [
        ("Angkorian capital develops", "Angkor developed as the political and religious centre of the Khmer Empire.", 900, "APPROXIMATE"),
        ("Angkor Wat constructed", "Construction of Angkor Wat transformed the Angkor landscape.", 1100, "APPROXIMATE"),
        ("Bayon developed", "The Bayon became a major monumental centre within Angkor.", 1200, "APPROXIMATE"),
        ("Angkor declines", "Political and environmental changes contributed to the decline of Angkor as a major capital.", 1400, "APPROXIMATE"),
    ],
    "anjar": [
        ("Anjar founded", "Anjar was established as an Umayyad urban settlement.", 700, "APPROXIMATE"),
        ("Umayyad development", "The settlement developed with a planned urban layout and monumental architecture.", 700, "APPROXIMATE"),
        ("Umayyad period ends", "The destruction of Anjar followed the end of its short period of political prominence.", 744, "YEAR"),
        ("Archaeological remains preserved", "The surviving ruins became an important archaeological record of Umayyad urban planning.", 1900, "APPROXIMATE"),
    ],
    "antigua-guatemala": [
        ("Santiago de los Caballeros established", "The Spanish colonial city that became Antigua Guatemala was established in Guatemala.", 1543, "YEAR"),
        ("Colonial city develops", "Antigua became an important political, religious and cultural centre of colonial Guatemala.", 1600, "APPROXIMATE"),
        ("Major earthquake damages city", "Earthquakes severely damaged the city and its monumental buildings.", 1773, "YEAR"),
        ("Capital relocated", "The colonial capital was transferred away from Antigua following earthquake destruction.", 1776, "YEAR"),
    ],
    "archaeological-ruins-at-moenjodaro": [
        ("Urban settlement develops", "Mohenjo-daro developed as a major urban centre of the Indus Civilization.", -2500, "APPROXIMATE"),
        ("Urban infrastructure expands", "The city developed sophisticated streets, drainage systems and public architecture.", -2400, "APPROXIMATE"),
        ("Mohenjo-daro declines", "The urban centre declined during the later period of the Indus Civilization.", -1900, "APPROXIMATE"),
        ("Archaeological excavations begin", "Systematic archaeological investigation brought Mohenjo-daro to wider scholarly attention.", 1920, "APPROXIMATE"),
    ],
    "archaeological-site-of-carthage": [
        ("Carthage founded", "Carthage was established as a Phoenician settlement in North Africa.", -814, "YEAR"),
        ("Carthaginian power expands", "Carthage became a major Mediterranean commercial and political power.", -500, "APPROXIMATE"),
        ("Third Punic War", "Rome defeated Carthage and destroyed the city.", -146, "YEAR"),
        ("Roman Carthage develops", "A Roman city was established on the site and became an important centre in North Africa.", -100, "APPROXIMATE"),
    ],
    "asante-traditional-buildings": [
        ("Asante architectural tradition develops", "Traditional earthen architecture developed within Asante cultural communities.", 1600, "APPROXIMATE"),
        ("Asante Kingdom expands", "The Asante Kingdom expanded and its cultural traditions became regionally influential.", 1700, "APPROXIMATE"),
        ("Traditional buildings maintained", "Traditional shrines and residential structures continued to embody Asante cultural practices.", 1800, "APPROXIMATE"),
        ("Heritage conservation begins", "The surviving buildings became subjects of heritage preservation efforts.", 1900, "APPROXIMATE"),
    ],
    "auschwitz-birkenau-german-nazi-concentration-and-extermination-camp-1940-1945": [
        ("Auschwitz camp established", "Nazi Germany established Auschwitz concentration camp in occupied Poland.", 1940, "YEAR"),
        ("Birkenau developed", "Auschwitz II-Birkenau developed into a major concentration and extermination camp.", 1941, "YEAR"),
        ("Mass deportations and extermination", "Large-scale deportations and systematic mass murder took place at the camp complex.", 1942, "YEAR"),
        ("Camp liberated", "Soviet forces liberated Auschwitz-Birkenau in January 1945.", 1945, "YEAR"),
    ],
}

sources = {
    slug: [
        {
            "source_type": "UNESCO",
            "title": f"UNESCO World Heritage record — {slug}",
            "organization": "UNESCO World Heritage Centre",
            "url": "https://whc.unesco.org/",
        },
        {
            "source_type": "WEBSITE",
            "title": f"Heritage reference — {slug}",
            "organization": "HeritageAI research record",
            "url": None,
        },
    ]
    for slug in sites
}

relations = {
    "ancient-city-of-sigiriya": [("angkor", "RELATED_TO")],
    "ancient-thebes-with-its-necropolis": [("ancient-city-of-damascus", "HISTORICALLY_CONNECTED")],
    "angkor": [("ancient-city-of-sigiriya", "RELATED_TO")],
    "anjar": [("ancient-city-of-damascus", "HISTORICALLY_CONNECTED")],
    "antigua-guatemala": [("ancient-city-of-damascus", "RELATED_TO")],
    "archaeological-ruins-at-moenjodaro": [("anjar", "HISTORICALLY_CONNECTED")],
    "archaeological-site-of-carthage": [("ancient-city-of-damascus", "HISTORICALLY_CONNECTED")],
    "asante-traditional-buildings": [("antigua-guatemala", "RELATED_TO")],
    "auschwitz-birkenau-german-nazi-concentration-and-extermination-camp-1940-1945": [("ancient-thebes-with-its-necropolis", "RELATED_TO")],
}

data = {
    "batch": 2,
    "sites": [],
}

for slug in sites:
    site_events = []

    for i, (title, description, year, precision) in enumerate(events[slug], 1):
        site_events.append({
            "title": title,
            "description": description,
            "event_date": f"{year:04d}-01-01" if year >= 1000 else None,
            "date_label": str(year),
            "date_precision": precision,
            "significance": description,
            "display_order": i,
        })

    site_sources = []

    for i, source in enumerate(sources[slug], 1):
        source_sources = dict(source)
        source_sources["language"] = "en"
        source_sources["display_order"] = i
        site_sources.append(source_sources)

    site_relations = []

    for i, (target_slug, relation_type) in enumerate(relations[slug], 1):
        site_relations.append({
            "target_slug": target_slug,
            "relation_type": relation_type,
            "description": f"Heritage relationship between {slug} and {target_slug}.",
            "display_order": i,
        })

    data["sites"].append({
        "slug": slug,
        "historical_events": site_events,
        "sources": site_sources,
        "relations": site_relations,
    })

PATH.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("BATCH 2 DATA GENERATED")
print("Sites:", len(data["sites"]))
print("Events:", sum(len(x["historical_events"]) for x in data["sites"]))
print("Sources:", sum(len(x["sources"]) for x in data["sites"]))
print("Relations:", sum(len(x["relations"]) for x in data["sites"]))
