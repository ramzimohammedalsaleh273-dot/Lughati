from pathlib import Path
from datetime import datetime
import shutil
from app.database import DB_PATH, engine, SessionLocal
from app.config import BACKUP_DIR

def backup_database():
    BACKUP_DIR.mkdir(parents=True,exist_ok=True)
    target=BACKUP_DIR/f"lughati_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    if not DB_PATH.exists():
        raise FileNotFoundError("قاعدة البيانات غير موجودة")
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA wal_checkpoint(FULL)")
    shutil.copy2(DB_PATH,target)
    return target

def restore_database(source):
    source=Path(source)
    if not source.exists(): raise FileNotFoundError("ملف النسخة الاحتياطية غير موجود")
    if source.resolve()==DB_PATH.resolve(): raise ValueError("اختر نسخة احتياطية مختلفة عن قاعدة البيانات الحالية")
    emergency=DB_PATH.with_name(f"{DB_PATH.stem}_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db")
    if DB_PATH.exists(): shutil.copy2(DB_PATH,emergency)
    engine.dispose()
    shutil.copy2(source,DB_PATH)
    return DB_PATH,emergency
