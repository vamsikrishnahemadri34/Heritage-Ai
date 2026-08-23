import json
from pathlib import Path

PATH = Path("batch1_enrichment.json")

data = json.loads(PATH.read_text(encoding="utf-8"))

records = {
    "aachen-cathedral": {
        "historical_events": [
            {
                "title": "Palatine Chapel constructed under Charlemagne",
                "description": "Construction of the Palatine Chapel at Aachen formed the core of the imperial palace complex associated with Charlemagne.",
                "event_date": None,
                "date_label": "c. 792-805",
                "date_precision": "APPROXIMATE",
                "display_order": 1,
                "significance": "Established the architectural core of the later Aachen Cathedral complex."
            },
            {
                "title": "Completion of the Palatine Chapel",
                "description": "The chapel was completed in the early ninth century and became an important monument of the Carolingian period.",
                "event_date": None,
                "date_label": "805",
                "date_precision": "YEAR",
                "display_order": 2,
                "significance": "The building became one of the most important surviving examples of Carolingian architecture."
            },
            {
                "title": "Aachen becomes an important pilgrimage centre",
                "description": "Aachen developed into an important pilgrimage destination associated with the relics preserved at the cathedral.",
                "event_date": None,
                "date_label": "Middle Ages",
                "date_precision": "PERIOD",
                "display_order": 3,
                "significance": "Strengthened the religious and cultural importance of the cathedral."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "Aachen Cathedral was inscribed on the UNESCO World Heritage List.",
                "event_date": "1978-01-01",
                "date_label": "1978",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized Aachen Cathedral as a heritage site of outstanding universal value."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Aachen Cathedral",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Aachen Cathedral",
                "organization": "German heritage authorities",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "chartres-cathedral",
                "relation_type": "RELATED_TO",
                "description": "Both are major European medieval cathedrals recognized for exceptional architectural and religious heritage.",
                "display_order": 1
            },
            {
                "target_slug": "mont-saint-michel-and-its-bay",
                "relation_type": "RELATED_TO",
                "description": "Both are major medieval European religious heritage complexes with enduring pilgrimage significance.",
                "display_order": 2
            }
        ]
    },

    "abu-mena": {
        "historical_events": [
            {
                "title": "Development of the Christian pilgrimage centre",
                "description": "The sanctuary of Saint Menas developed into an important Christian pilgrimage centre in late antiquity.",
                "event_date": None,
                "date_label": "4th-6th centuries CE",
                "date_precision": "PERIOD",
                "display_order": 1,
                "significance": "Established Abu Mena as one of the major pilgrimage centres of the early Christian world."
            },
            {
                "title": "Expansion of the pilgrimage complex",
                "description": "The sanctuary expanded with churches, accommodation, baths and other facilities serving pilgrims.",
                "event_date": None,
                "date_label": "5th-6th centuries CE",
                "date_precision": "PERIOD",
                "display_order": 2,
                "significance": "Demonstrates the scale and organization of early Christian pilgrimage infrastructure."
            },
            {
                "title": "Decline of the ancient pilgrimage centre",
                "description": "The ancient settlement and pilgrimage centre declined over subsequent centuries.",
                "event_date": None,
                "date_label": "7th-9th centuries CE",
                "date_precision": "PERIOD",
                "display_order": 3,
                "significance": "Preserved archaeological evidence of the transformation of the late antique Christian landscape."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "Abu Mena was inscribed on the UNESCO World Heritage List.",
                "event_date": "1979-01-01",
                "date_label": "1979",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized the archaeological site as having outstanding universal value."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Abu Mena",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Abu Mena",
                "organization": "Egyptian heritage authorities",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "ancient-city-of-damascus",
                "relation_type": "RELATED_TO",
                "description": "Both preserve important archaeological evidence of the ancient and early Christian Near Eastern cultural landscape.",
                "display_order": 1
            },
            {
                "target_slug": "aachen-cathedral",
                "relation_type": "RELATED_TO",
                "description": "Both are major Christian heritage sites whose historical importance includes religious pilgrimage traditions.",
                "display_order": 2
            }
        ]
    },

    "agra-fort": {
        "historical_events": [
            {
                "title": "Mughal transformation of Agra Fort begins",
                "description": "Emperor Akbar began rebuilding the earlier fortification at Agra in red sandstone.",
                "event_date": "1565-01-01",
                "date_label": "1565",
                "date_precision": "YEAR",
                "display_order": 1,
                "significance": "Established the monumental Mughal fort complex visible today."
            },
            {
                "title": "Expansion under Mughal emperors",
                "description": "Successive Mughal rulers expanded and modified the fort with palaces, audience halls and other imperial structures.",
                "event_date": None,
                "date_label": "16th-17th centuries",
                "date_precision": "PERIOD",
                "display_order": 2,
                "significance": "Created a layered architectural record of Mughal imperial development."
            },
            {
                "title": "Agra Fort becomes an imperial residence",
                "description": "The fort served as a major imperial residence and administrative centre of the Mughal Empire.",
                "event_date": None,
                "date_label": "16th-17th centuries",
                "date_precision": "PERIOD",
                "display_order": 3,
                "significance": "Reflects the political and cultural importance of Agra during the Mughal period."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "Agra Fort was inscribed on the UNESCO World Heritage List.",
                "event_date": "1983-01-01",
                "date_label": "1983",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized the fort as a monument of outstanding universal value."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Agra Fort",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Agra Fort",
                "organization": "Archaeological Survey of India",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "taj-mahal",
                "relation_type": "ASSOCIATED_WITH",
                "description": "Both are major Mughal monuments in Agra associated with the imperial architectural tradition.",
                "display_order": 1
            },
            {
                "target_slug": "red-fort",
                "relation_type": "RELATED_TO",
                "description": "Both are major Mughal imperial fort complexes in northern India.",
                "display_order": 2
            }
        ]
    },

    "aksum": {
        "historical_events": [
            {
                "title": "Rise of the Aksumite civilization",
                "description": "Aksum developed into the centre of a powerful ancient civilization in the northern Ethiopian highlands.",
                "event_date": None,
                "date_label": "1st-4th centuries CE",
                "date_precision": "PERIOD",
                "display_order": 1,
                "significance": "Established Aksum as a major political and commercial power in the ancient Red Sea region."
            },
            {
                "title": "Development of monumental stelae",
                "description": "The Aksumite civilization erected monumental stone stelae associated with elite burials and royal monuments.",
                "event_date": None,
                "date_label": "4th century CE",
                "date_precision": "PERIOD",
                "display_order": 2,
                "significance": "The stelae represent exceptional achievements in ancient African monumental architecture."
            },
            {
                "title": "Adoption of Christianity",
                "description": "Christianity became established in the Aksumite kingdom during the fourth century.",
                "event_date": None,
                "date_label": "4th century CE",
                "date_precision": "PERIOD",
                "display_order": 3,
                "significance": "Marked a major transformation in the religious history of the Aksumite civilization."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "Aksum was inscribed on the UNESCO World Heritage List.",
                "event_date": "1980-01-01",
                "date_label": "1980",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized Aksum's outstanding archaeological and cultural importance."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Aksum",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Aksum",
                "organization": "Ethiopian heritage authorities",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "al-qal-a-of-beni-hammad",
                "relation_type": "RELATED_TO",
                "description": "Both preserve archaeological evidence of major historic African centres of political and cultural development.",
                "display_order": 1
            },
            {
                "target_slug": "ancient-city-of-bosra",
                "relation_type": "RELATED_TO",
                "description": "Both were important historic centres connected to ancient trade and cultural exchange networks.",
                "display_order": 2
            }
        ]
    },

    "al-qal-a-of-beni-hammad": {
        "historical_events": [
            {
                "title": "Foundation of the Hammadid capital",
                "description": "The Hammadid ruler Hammad ibn Buluggin founded Al Qal'a of Beni Hammad as a fortified capital.",
                "event_date": "1007-01-01",
                "date_label": "1007",
                "date_precision": "YEAR",
                "display_order": 1,
                "significance": "Established one of the major fortified political centres of medieval North Africa."
            },
            {
                "title": "Development of the Hammadid capital",
                "description": "The settlement expanded with palaces, religious buildings, defensive structures and urban facilities.",
                "event_date": None,
                "date_label": "11th century",
                "date_precision": "PERIOD",
                "display_order": 2,
                "significance": "Provides important evidence of medieval Islamic urban and architectural development."
            },
            {
                "title": "Destruction and abandonment",
                "description": "The fortified capital was destroyed and subsequently abandoned after attacks by the Almohads.",
                "event_date": None,
                "date_label": "1152",
                "date_precision": "YEAR",
                "display_order": 3,
                "significance": "The abandonment preserved extensive archaeological evidence of the Hammadid capital."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "Al Qal'a of Beni Hammad was inscribed on the UNESCO World Heritage List.",
                "event_date": "1980-01-01",
                "date_label": "1980",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized the archaeological remains as having outstanding universal value."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Al Qal'a of Beni Hammad",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Al Qal'a of Beni Hammad",
                "organization": "Algerian cultural heritage authorities",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "aksum",
                "relation_type": "RELATED_TO",
                "description": "Both preserve archaeological remains of important historic African political centres.",
                "display_order": 1
            },
            {
                "target_slug": "ancient-city-of-bosra",
                "relation_type": "RELATED_TO",
                "description": "Both preserve substantial archaeological evidence of historic urban centres in the wider Near Eastern and North African region.",
                "display_order": 2
            }
        ]
    },

    "amphitheatre-of-el-jem": {
        "historical_events": [
            {
                "title": "Construction of the Roman amphitheatre",
                "description": "The monumental amphitheatre at El Jem was constructed during the Roman period.",
                "event_date": None,
                "date_label": "3rd century CE",
                "date_precision": "PERIOD",
                "display_order": 1,
                "significance": "Created one of the largest and best-preserved Roman amphitheatres in North Africa."
            },
            {
                "title": "El Jem becomes a major Roman urban centre",
                "description": "The settlement developed as an important centre in the Roman province of Africa Proconsularis.",
                "event_date": None,
                "date_label": "Roman period",
                "date_precision": "PERIOD",
                "display_order": 2,
                "significance": "Demonstrates the economic and urban importance of the region during Roman rule."
            },
            {
                "title": "Preservation of the monumental amphitheatre",
                "description": "The amphitheatre survived with substantial portions of its original monumental structure.",
                "event_date": None,
                "date_label": "Modern period",
                "date_precision": "PERIOD",
                "display_order": 3,
                "significance": "Provides exceptional evidence of Roman public architecture in North Africa."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "The Amphitheatre of El Jem was inscribed on the UNESCO World Heritage List.",
                "event_date": "1979-01-01",
                "date_label": "1979",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized the monument's outstanding universal value."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Amphitheatre of El Jem",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Amphitheatre of El Jem",
                "organization": "Tunisian cultural heritage authorities",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "ancient-city-of-bosra",
                "relation_type": "RELATED_TO",
                "description": "Both preserve major Roman-period monuments associated with historic urban centres.",
                "display_order": 1
            },
            {
                "target_slug": "aachen-cathedral",
                "relation_type": "RELATED_TO",
                "description": "Both illustrate major architectural achievements from different periods of European and Mediterranean history.",
                "display_order": 2
            }
        ]
    },

    "ancient-city-of-bosra": {
        "historical_events": [
            {
                "title": "Bosra becomes an important Nabataean centre",
                "description": "Bosra developed as an important settlement and regional centre during the Nabataean period.",
                "event_date": None,
                "date_label": "Nabataean period",
                "date_precision": "PERIOD",
                "display_order": 1,
                "significance": "Demonstrates Bosra's position within the political and commercial networks of the ancient Near East."
            },
            {
                "title": "Roman annexation and development",
                "description": "Bosra became part of the Roman Empire and developed into a major urban centre.",
                "event_date": "106-01-01",
                "date_label": "106 CE",
                "date_precision": "YEAR",
                "display_order": 2,
                "significance": "Roman development produced major monuments that remain central to the site's archaeological importance."
            },
            {
                "title": "Bosra becomes an important Christian centre",
                "description": "During late antiquity Bosra developed important Christian institutions and religious architecture.",
                "event_date": None,
                "date_label": "4th-6th centuries CE",
                "date_precision": "PERIOD",
                "display_order": 3,
                "significance": "Reflects the religious transformation of the ancient Near East."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "The Ancient City of Bosra was inscribed on the UNESCO World Heritage List.",
                "event_date": "1980-01-01",
                "date_label": "1980",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized Bosra's exceptional archaeological and architectural heritage."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Ancient City of Bosra",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Ancient City of Bosra",
                "organization": "Syrian cultural heritage authorities",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "ancient-city-of-damascus",
                "relation_type": "RELATED_TO",
                "description": "Both are major historic cities in Syria with long archaeological and cultural histories.",
                "display_order": 1
            },
            {
                "target_slug": "al-qal-a-of-beni-hammad",
                "relation_type": "RELATED_TO",
                "description": "Both preserve important archaeological evidence of historic urban development in the wider Islamic and Mediterranean world.",
                "display_order": 2
            }
        ]
    },

    "ancient-city-of-damascus": {
        "historical_events": [
            {
                "title": "Ancient settlement develops at Damascus",
                "description": "Damascus developed as one of the long-lived urban centres of the Near East.",
                "event_date": None,
                "date_label": "2nd millennium BCE and earlier",
                "date_precision": "PERIOD",
                "display_order": 1,
                "significance": "Demonstrates the exceptional continuity of urban settlement in the region."
            },
            {
                "title": "Damascus becomes an important Aramaean centre",
                "description": "Damascus became an important political centre of the Aramaean kingdom.",
                "event_date": None,
                "date_label": "1st millennium BCE",
                "date_precision": "PERIOD",
                "display_order": 2,
                "significance": "Established Damascus as a major political centre in the ancient Levant."
            },
            {
                "title": "Damascus develops under Roman and Byzantine rule",
                "description": "The city continued to develop as an important urban centre under Roman and Byzantine rule.",
                "event_date": None,
                "date_label": "Roman and Byzantine periods",
                "date_precision": "PERIOD",
                "display_order": 3,
                "significance": "Created layers of cultural heritage that contributed to Damascus's exceptional historical continuity."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "The Ancient City of Damascus was inscribed on the UNESCO World Heritage List.",
                "event_date": "1979-01-01",
                "date_label": "1979",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized Damascus as a heritage site of outstanding universal value."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Ancient City of Damascus",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Ancient City of Damascus",
                "organization": "Syrian cultural heritage authorities",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "ancient-city-of-bosra",
                "relation_type": "RELATED_TO",
                "description": "Both are major historic Syrian cities preserving extensive archaeological and architectural heritage.",
                "display_order": 1
            },
            {
                "target_slug": "abu-mena",
                "relation_type": "RELATED_TO",
                "description": "Both preserve important evidence of the historical and religious development of the eastern Mediterranean region.",
                "display_order": 2
            }
        ]
    },

    "ancient-city-of-polonnaruwa": {
        "historical_events": [
            {
                "title": "Polonnaruwa becomes the Sri Lankan royal capital",
                "description": "Polonnaruwa became a major royal capital following the decline of Anuradhapura.",
                "event_date": None,
                "date_label": "11th century CE",
                "date_precision": "PERIOD",
                "display_order": 1,
                "significance": "Established Polonnaruwa as one of the principal political centres of medieval Sri Lanka."
            },
            {
                "title": "Development under Parakramabahu I",
                "description": "King Parakramabahu I expanded the city with monumental architecture, religious complexes and extensive hydraulic works.",
                "event_date": None,
                "date_label": "12th century CE",
                "date_precision": "PERIOD",
                "display_order": 2,
                "significance": "The period produced many of the site's most important surviving monuments."
            },
            {
                "title": "Development of major Buddhist monuments",
                "description": "Large Buddhist monuments and religious institutions were developed across the royal city.",
                "event_date": None,
                "date_label": "12th century CE",
                "date_precision": "PERIOD",
                "display_order": 3,
                "significance": "Demonstrates the importance of Buddhism and monumental architecture in medieval Sri Lanka."
            },
            {
                "title": "UNESCO World Heritage inscription",
                "description": "The Ancient City of Polonnaruwa was inscribed on the UNESCO World Heritage List.",
                "event_date": "1982-01-01",
                "date_label": "1982",
                "date_precision": "YEAR",
                "display_order": 4,
                "significance": "Recognized the archaeological city as having outstanding universal value."
            }
        ],
        "sources": [
            {
                "source_type": "UNESCO",
                "title": "Ancient City of Polonnaruwa",
                "organization": "UNESCO World Heritage Centre",
                "display_order": 1
            },
            {
                "source_type": "GOVERNMENT",
                "title": "Ancient City of Polonnaruwa",
                "organization": "Sri Lankan cultural heritage authorities",
                "display_order": 2
            }
        ],
        "relations": [
            {
                "target_slug": "ancient-city-of-damascus",
                "relation_type": "RELATED_TO",
                "description": "Both preserve historic urban centres with long architectural and religious traditions.",
                "display_order": 1
            },
            {
                "target_slug": "abu-mena",
                "relation_type": "RELATED_TO",
                "description": "Both preserve important archaeological landscapes shaped by historic religious traditions.",
                "display_order": 2
            }
        ]
    }
}

for site in data["sites"]:
    slug = site["slug"]
    if slug not in records:
        raise ValueError(f"Missing enrichment records for {slug}")

    site["historical_events"] = records[slug]["historical_events"]
    site["sources"] = records[slug]["sources"]
    site["relations"] = records[slug]["relations"]

PATH.write_text(
    json.dumps(data, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("BATCH 1 DATA GENERATED")
print("Sites:", len(data["sites"]))
print("Events:", sum(len(x["historical_events"]) for x in data["sites"]))
print("Sources:", sum(len(x["sources"]) for x in data["sites"]))
print("Relations:", sum(len(x["relations"]) for x in data["sites"]))
