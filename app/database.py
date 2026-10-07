from pathlib import Path
from sqlalchemy import create_engine,event
from sqlalchemy.orm import declarative_base,sessionmaker

ROOT=Path(__file__).resolve().parent.parent
DATA_DIR=ROOT/"data"; DATA_DIR.mkdir(parents=True,exist_ok=True)
DB_PATH=DATA_DIR/"lughati.db"
engine=create_engine(f"sqlite:///{DB_PATH}",future=True)
@event.listens_for(engine,"connect")
def _sqlite_pragmas(dbapi_connection,connection_record):
    cursor=dbapi_connection.cursor(); cursor.execute("PRAGMA foreign_keys=ON"); cursor.execute("PRAGMA journal_mode=WAL"); cursor.execute("PRAGMA synchronous=NORMAL"); cursor.close()
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,expire_on_commit=False)
Base=declarative_base()

def init_db():
    from app.models import Base as ModelBase
    ModelBase.metadata.create_all(engine)
    with engine.begin() as conn:
        cols=[row[1] for row in conn.exec_driver_sql("PRAGMA table_info(daily_plans)").fetchall()]
        if "tasks" not in cols: conn.exec_driver_sql("ALTER TABLE daily_plans ADD COLUMN tasks TEXT DEFAULT '[]'")
    from app.migrations import ensure_schema
    ensure_schema()
