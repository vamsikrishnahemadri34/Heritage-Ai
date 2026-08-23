import json

with open("unesco_world_heritage.json", encoding="utf-8") as f:
    data = json.load(f)

target = "Buddhist Ruins of Takht-i-Bahi and Neighbouring City Remains at Sahr-i-Bahlol"

for x in data:
    if x.get("name_en") == target:
        print("FOUND UNESCO RECORD")
        print("===================")
        print("NAME:", x.get("name_en"))
        print("MAIN IMAGE:", x.get("main_image_url"))
        print("IMAGES URLS:", x.get("images_urls"))
        print("VIDEO:", x.get("main_video_url"))
        print("UUID:", x.get("uuid"))
        print("ID:", x.get("id_no"))
        break
else:
    print("NOT FOUND")
