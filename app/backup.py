from pathlib import Path
import shutil
from app.database import DB_PATH
from app.config import BACKUP_DIR

def backup_database():
    BACKUP_DIR.mkdir(exist_ok=True)
    target=BACKUP_DIR/("lughati_"+__import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")+".db")
    if DB_PATH.exists(): shutil.copy2(DB_PATH,target)
    return target

def restore_database(source):
    source=Path(source)
    if not source.exists(): raise FileNotFoundError("ملف النسخة الاحتياطية غير موجود")
    if DB_PATH.exists(): shutil.copy2(DB_PATH,DB_PATH.with_suffix(".before_restore.db"))
    shutil.copy2(source,DB_PATH)
    return DB_PATH
