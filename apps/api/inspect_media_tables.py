from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    print("MEDIA TABLES")
    print("============")

    tables = conn.execute(
        text("SHOW TABLES")
    ).fetchall()

    for table in tables:
        name = list(table)[0]

        if "media" in name.lower():
            print("\nTABLE:", name)

            rows = conn.execute(
                text(f"SHOW COLUMNS FROM `{name}`")
            ).fetchall()

            for row in rows:
                print(
                    f"{row.Field} | "
                    f"type={row.Type} | "
                    f"null={row.Null} | "
                    f"default={row.Default} | "
                    f"key={row.Key}"
                )
