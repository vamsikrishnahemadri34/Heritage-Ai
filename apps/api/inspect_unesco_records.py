import json

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    data = json.load(f)

ids = {
    "404",
    "668",
    "31",
    "250",
    "241",
    "246",
    "274",
    "231",
}

for record in data:
    if str(record.get("id_no")) in ids:
        print("=" * 80)
        print("ID           :", record.get("id_no"))
        print("NAME         :", record.get("name_en"))
        print("COUNTRY      :", record.get("country"))
        print("DATE         :", record.get("date_inscribed"))
        print("CATEGORY     :", record.get("category"))
        print("LATITUDE     :", record.get("latitude"))
        print("LONGITUDE    :", record.get("longitude"))
        print("DESCRIPTION  :", record.get("description"))
        print("UUID         :", record.get("unesco_uuid"))
        print("IMAGE URL    :", record.get("main_image_url"))
