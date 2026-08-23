from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

tables = [
    "heritage_site_historical_events",
    "heritage_site_sources",
    "heritage_site_relations",
]

with engine.connect() as conn:
    for table in tables:
        print()
        print("=" * 70)
        print(f"TABLE: {table}")
        print("=" * 70)

        rows = conn.execute(
            text(f"SHOW COLUMNS FROM {table}")
        ).fetchall()

        for row in rows:
            print(
                f"{row.Field} | "
                f"type={row.Type} | "
                f"null={row.Null} | "
                f"default={row.Default} | "
                f"key={row.Key}"
            )
