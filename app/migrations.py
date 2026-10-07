from sqlalchemy import inspect, text
from app.database import engine, Base

SCHEMA_VERSION=2

def ensure_schema():
    Base.metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS app_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)"))
        row=conn.execute(text("SELECT value FROM app_meta WHERE key='schema_version'")).fetchone()
        current=int(row[0]) if row else 0
        if current < SCHEMA_VERSION:
            conn.execute(text("INSERT OR REPLACE INTO app_meta(key,value) VALUES('schema_version', :v)"), {"v":str(SCHEMA_VERSION)})
    return SCHEMA_VERSION

def schema_info():
    inspector=inspect(engine)
    return {"version":SCHEMA_VERSION,"tables":sorted(inspector.get_table_names())}
