from pathlib import Path

sites = [
    "Aachen Cathedral",
    "Abu Mena",
    "Agra Fort",
    "Aksum",
    "Al Qal'a of Beni Hammad",
    "Amphitheatre of El Jem",
    "Ancient City of Bosra",
    "Ancient City of Damascus",
    "Ancient City of Polonnaruwa",
]

print("=" * 80)
print("HERITAGEAI - BATCH 1 ENRICHMENT")
print("=" * 80)

for i, site in enumerate(sites, 1):
    print(f"{i}. {site}")

print()
print("TARGET:")
print("9 sites")
print("36 historical events")
print("18 sources")
print("18 relations")
print()
print("DATABASE WILL NOT BE MODIFIED BY THIS STEP.")
