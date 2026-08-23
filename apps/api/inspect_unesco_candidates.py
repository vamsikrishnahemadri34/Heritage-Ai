import json

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    data = json.load(f)

terms = [
    "Angkor Wat",
    "Brihadeeswarar",
    "Hampi",
    "Angkor",
    "Chola",
    "Vijayanagara",
]

for record in data:
    name = record.get("name_en") or ""

    if any(term.lower() in name.lower() for term in terms):
        print(
            f"ID={record.get('id_no')} | {name}"
        )
