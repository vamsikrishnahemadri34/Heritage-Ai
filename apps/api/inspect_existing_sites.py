from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as connection:
    rows = connection.execute(
        text("""
            SELECT id, name, slug, country, city, latitude, longitude
            FROM heritage_sites
            ORDER BY name
        """)
    ).fetchall()

print("EXISTING SITES:", len(rows))
print()

for i, row in enumerate(rows, 1):
    print(
        f"{i}. {row.name} | "
        f"{row.country} | "
        f"{row.city or '-'} | "
        f"{row.latitude} | {row.longitude} | "
        f"{row.slug}"
    )
