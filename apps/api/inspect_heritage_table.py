from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    rows = conn.execute(
        text("SHOW COLUMNS FROM heritage_sites")
    ).fetchall()

    print("HERITAGE_SITES TABLE")
    print("====================")

    for row in rows:
        print(
            f"{row.Field} | "
            f"type={row.Type} | "
            f"null={row.Null} | "
            f"default={row.Default} | "
            f"key={row.Key}"
        )
