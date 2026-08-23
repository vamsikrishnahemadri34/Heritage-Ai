import json
import uuid
from datetime import date
from sqlalchemy import create_engine, text

from app.core.config import settings


JSON_PATH = "batch1_enrichment.json"

engine = create_engine(settings.DATABASE_URL)


def parse_date(value):
    if not value:
        return None
    parts = value.split("-")

    if len(parts[0]) == 4:
        return date.fromisoformat(value)

    return date(
        int(parts[0]),
        int(parts[1]),
        int(parts[2]),
    )


with open(JSON_PATH, encoding="utf-8") as f:
    data = json.load(f)

sites = data["sites"]

expected_events = sum(len(s["historical_events"]) for s in sites)
expected_sources = sum(len(s["sources"]) for s in sites)
expected_relations = sum(len(s["relations"]) for s in sites)

print("=" * 70)
print("HERITAGEAI - BATCH 1 IMPORT")
print("=" * 70)
print(f"SITES     : {len(sites)}")
print(f"EVENTS    : {expected_events}")
print(f"SOURCES   : {expected_sources}")
print(f"RELATIONS : {expected_relations}")
print()

with engine.begin() as conn:

    site_rows = conn.execute(
        text("""
            SELECT id, slug
            FROM heritage_sites
            WHERE slug IN :slugs
        """),
        {"slugs": tuple(s["slug"] for s in sites)},
    ).fetchall()

    site_map = {row.slug: row.id for row in site_rows}

    missing = [
        s["slug"]
        for s in sites
        if s["slug"] not in site_map
    ]

    if missing:
        raise RuntimeError(
            f"Missing sites: {missing}"
        )

    # Prevent accidental duplicate import.
    existing_events = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM heritage_site_historical_events
            WHERE site_id IN :site_ids
        """),
        {"site_ids": tuple(site_map.values())},
    ).scalar()

    existing_sources = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM heritage_site_sources
            WHERE site_id IN :site_ids
        """),
        {"site_ids": tuple(site_map.values())},
    ).scalar()

    existing_relations = conn.execute(
        text("""
            SELECT COUNT(*)
            FROM heritage_site_relations
            WHERE source_site_id IN :site_ids
        """),
        {"site_ids": tuple(site_map.values())},
    ).scalar()

    if existing_events or existing_sources or existing_relations:
        raise RuntimeError(
            "ABORTED: Batch sites already contain enrichment records. "
            f"events={existing_events}, "
            f"sources={existing_sources}, "
            f"relations={existing_relations}"
        )

    # Resolve relation targets.
    target_slugs = {
        relation["target_slug"]
        for site in sites
        for relation in site["relations"]
    }

    target_rows = conn.execute(
        text("""
            SELECT id, slug
            FROM heritage_sites
            WHERE slug IN :slugs
        """),
        {"slugs": tuple(target_slugs)},
    ).fetchall()

    target_map = {row.slug: row.id for row in target_rows}

    missing_targets = target_slugs - set(target_map)

    if missing_targets:
        raise RuntimeError(
            f"Missing relation targets: {sorted(missing_targets)}"
        )

    # EVENTS
    for site in sites:
        site_id = site_map[site["slug"]]

        for event in site["historical_events"]:
            conn.execute(
                text("""
                    INSERT INTO heritage_site_historical_events (
                        id,
                        site_id,
                        title,
                        description,
                        event_date,
                        date_label,
                        date_precision,
                        significance,
                        display_order,
                        is_verified,
                        is_active,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :id,
                        :site_id,
                        :title,
                        :description,
                        :event_date,
                        :date_label,
                        :date_precision,
                        :significance,
                        :display_order,
                        :is_verified,
                        :is_active,
                        NOW(),
                        NOW()
                    )
                """),
                {
                    "id": str(uuid.uuid4()),
                    "site_id": site_id,
                    "title": event["title"],
                    "description": event.get("description"),
                    "event_date": parse_date(event.get("event_date")),
                    "date_label": event.get("date_label"),
                    "date_precision": event["date_precision"],
                    "significance": event.get("significance"),
                    "display_order": event["display_order"],
                    "is_verified": False,
                    "is_active": True,
                },
            )

    # SOURCES
    for site in sites:
        site_id = site_map[site["slug"]]

        for source in site["sources"]:
            conn.execute(
                text("""
                    INSERT INTO heritage_site_sources (
                        id,
                        site_id,
                        source_type,
                        title,
                        author,
                        organization,
                        publisher,
                        publication_date,
                        url,
                        citation_text,
                        language,
                        display_order,
                        is_verified,
                        is_active,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :id,
                        :site_id,
                        :source_type,
                        :title,
                        :author,
                        :organization,
                        :publisher,
                        :publication_date,
                        :url,
                        :citation_text,
                        :language,
                        :display_order,
                        :is_verified,
                        :is_active,
                        NOW(),
                        NOW()
                    )
                """),
                {
                    "id": str(uuid.uuid4()),
                    "site_id": site_id,
                    "source_type": source["source_type"],
                    "title": source["title"],
                    "author": source.get("author"),
                    "organization": source.get("organization"),
                    "publisher": source.get("publisher"),
                    "publication_date": parse_date(
                        source.get("publication_date")
                    ),
                    "url": source.get("url"),
                    "citation_text": source.get("citation_text"),
                    "language": source.get("language", "en"),
                    "display_order": source["display_order"],
                    "is_verified": False,
                    "is_active": True,
                },
            )

    # RELATIONS
    for site in sites:
        source_site_id = site_map[site["slug"]]

        for relation in site["relations"]:
            conn.execute(
                text("""
                    INSERT INTO heritage_site_relations (
                        id,
                        source_site_id,
                        target_site_id,
                        relation_type,
                        description,
                        display_order,
                        is_verified,
                        is_active,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :id,
                        :source_site_id,
                        :target_site_id,
                        :relation_type,
                        :description,
                        :display_order,
                        :is_verified,
                        :is_active,
                        NOW(),
                        NOW()
                    )
                """),
                {
                    "id": str(uuid.uuid4()),
                    "source_site_id": source_site_id,
                    "target_site_id": target_map[
                        relation["target_slug"]
                    ],
                    "relation_type": relation["relation_type"],
                    "description": relation.get("description"),
                    "display_order": relation["display_order"],
                    "is_verified": False,
                    "is_active": True,
                },
            )

print("IMPORT COMMITTED")
print("Events inserted    :", expected_events)
print("Sources inserted   :", expected_sources)
print("Relations inserted :", expected_relations)

