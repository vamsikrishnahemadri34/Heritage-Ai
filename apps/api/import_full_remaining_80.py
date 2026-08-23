import json
import uuid
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.heritage_site_source import HeritageSiteSource, SourceType
from app.models.heritage_site_media import HeritageSiteMedia, MediaType
from app.models.heritage_site_relation import HeritageSiteRelation, RelationType

engine = create_engine(settings.DATABASE_URL)

with open("full_remaining_80_sources_media_preview.json", encoding="utf-8") as f:
    sm = json.load(f)

with open("full_remaining_80_relations_preview.json", encoding="utf-8") as f:
    rel = json.load(f)

sites = {x["slug"]: x for x in sm["sites"]}
relations = {x["slug"]: x for x in rel["sites"]}

if len(sites) != 80:
    raise ValueError(f"Expected 80 sites, got {len(sites)}")

if len(relations) != 80:
    raise ValueError(f"Expected 80 relation records, got {len(relations)}")

source_total = sum(len(x["sources"]) for x in sites.values())
video_total = sum(len(x["media"]) for x in sites.values())
relation_total = sum(len(x["relations"]) for x in relations.values())

if source_total != 80:
    raise ValueError(f"Expected 80 sources, got {source_total}")

if relation_total != 160:
    raise ValueError(f"Expected 160 relations, got {relation_total}")

print("=" * 80)
print("HERITAGEAI — FULL REMAINING 80 IMPORT")
print("=" * 80)
print("Sites     :", len(sites))
print("Sources   :", source_total)
print("Videos    :", video_total)
print("Relations :", relation_total)
print()
print("Starting transaction...")

with Session(engine) as db:

    try:

        # Resolve every site against the database first.
        db_sites = {}

        for slug in sites:

            row = db.execute(
                text("""
                    SELECT id
                    FROM heritage_sites
                    WHERE slug = :slug
                    LIMIT 1
                """),
                {"slug": slug},
            ).mappings().first()

            if row is None:
                raise ValueError(
                    f"Database site not found: {slug}"
                )

            db_sites[slug] = row["id"]

        # Prevent duplicate imports.
        for slug, site_id in db_sites.items():

            existing_source = db.execute(
                text("""
                    SELECT COUNT(*)
                    FROM heritage_site_sources
                    WHERE site_id = :site_id
                      AND source_type = 'UNESCO'
                """),
                {"site_id": site_id},
            ).scalar()

            if existing_source:
                raise ValueError(
                    f"UNESCO source already exists: {slug}"
                )

        inserted_sources = 0
        inserted_videos = 0
        inserted_relations = 0

        # SOURCES + VIDEOS
        for slug, site in sites.items():

            site_id = db_sites[slug]

            for source in site["sources"]:

                db.add(
                    HeritageSiteSource(
                        id=str(uuid.uuid4()),
                        site_id=site_id,
                        source_type=SourceType(source["source_type"]),
                        title=source["title"],
                        author=source.get("author"),
                        organization=source.get("organization"),
                        publisher=source.get("publisher"),
                        publication_date=None,
                        url=source.get("url"),
                        citation_text=source.get("citation_text"),
                        language=source.get("language", "en"),
                        display_order=source.get("display_order", 0),
                        is_verified=source.get("is_verified", False),
                        is_active=source.get("is_active", True),
                    )
                )

                inserted_sources += 1

            for media in site["media"]:

                db.add(
                    HeritageSiteMedia(
                        id=str(uuid.uuid4()),
                        site_id=site_id,
                        media_type=MediaType(media["media_type"]),
                        storage_key=media["storage_key"],
                        url=media["url"],
                        title=media.get("title"),
                        alt_text=media.get("alt_text"),
                        display_order=media.get("display_order", 0),
                        is_primary=media.get("is_primary", False),
                        is_active=media.get("is_active", True),
                    )
                )

                inserted_videos += 1

        # RELATIONS
        for slug, site in relations.items():

            source_site_id = db_sites[slug]

            for relation in site["relations"]:

                target_slug = relation["target_slug"]

                if target_slug not in db_sites:
                    raise ValueError(
                        f"Relation target not in import set: "
                        f"{slug} -> {target_slug}"
                    )

                target_site_id = db_sites[target_slug]

                if source_site_id == target_site_id:
                    raise ValueError(
                        f"Self relation detected: {slug}"
                    )

                db.add(
                    HeritageSiteRelation(
                        id=str(uuid.uuid4()),
                        source_site_id=source_site_id,
                        target_site_id=target_site_id,
                        relation_type=RelationType(
                            relation["relation_type"]
                        ),
                        description=relation.get("description"),
                        display_order=relation.get("display_order", 0),
                        is_verified=False,
                        is_active=True,
                    )
                )

                inserted_relations += 1

        db.flush()

        print()
        print("FLUSH VALIDATION")
        print("Sources inserted   :", inserted_sources)
        print("Videos inserted    :", inserted_videos)
        print("Relations inserted :", inserted_relations)

        if inserted_sources != 80:
            raise ValueError("Source count validation failed")

        if inserted_videos != video_total:
            raise ValueError("Video count validation failed")

        if inserted_relations != 160:
            raise ValueError("Relation count validation failed")

        db.commit()

        print()
        print("=" * 80)
        print("IMPORT COMMITTED")
        print("=" * 80)
        print("Sources inserted   :", inserted_sources)
        print("Videos inserted    :", inserted_videos)
        print("Relations inserted :", inserted_relations)

    except Exception:
        db.rollback()
        print()
        print("=" * 80)
        print("IMPORT FAILED — ROLLED BACK")
        print("=" * 80)
        raise
