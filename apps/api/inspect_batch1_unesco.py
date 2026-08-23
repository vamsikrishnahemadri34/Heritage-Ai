import json

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    records = json.load(f)

targets = {
    "Aachen Cathedral",
    "Abu Mena",
    "Agra Fort",
    "Aksum",
    "Al Qal'a of Beni Hammad",
    "Amphitheatre of El Jem",
    "Ancient City of Bosra",
    "Ancient City of Damascus",
    "Ancient City of Polonnaruwa",
}

for record in records:
    name = (record.get("name_en") or "").strip()

    if name in targets:
        print("=" * 80)
        print("NAME       :", name)
        print("ID         :", record.get("id_no"))
        print("DATE       :", record.get("date_inscribed"))
        print("CATEGORY   :", record.get("category"))
        print("COUNTRY    :", record.get("country"))
        print("LATITUDE   :", record.get("latitude"))
        print("LONGITUDE  :", record.get("longitude"))
        print("DESCRIPTION:", record.get("short_description") or record.get("description"))
        print()
