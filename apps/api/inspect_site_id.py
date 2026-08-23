from sqlalchemy import create_engine, text
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)

with engine.connect() as conn:
    rows = conn.execute(
        text("""
            SHOW COLUMNS FROM heritage_sites
            WHERE Field = 'id'
        """)
    ).fetchall()

    for row in rows:
        print(row)
