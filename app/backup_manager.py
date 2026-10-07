"""نسخ احتياطي واستعادة آمنة باستخدام SQLite Online Backup."""
from pathlib import Path
from datetime import datetime
import sqlite3
from app.config import BACKUP_DIR
from app.database import DB_PATH
from app.database import engine, init_db
VERSION=1

def backup_database_safe(target=None):
    BACKUP_DIR.mkdir(parents=True,exist_ok=True)
    target=Path(target) if target else BACKUP_DIR/f"lughati_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    if not DB_PATH.exists(): raise FileNotFoundError("قاعدة البيانات غير موجودة")
    engine.dispose()
    src=sqlite3.connect(str(DB_PATH)); dst=sqlite3.connect(str(target))
    try: src.backup(dst); dst.commit()
    finally: dst.close(); src.close()
    check=validate_backup(target)
    if not check["ok"]: target.unlink(missing_ok=True); raise RuntimeError("فشل التحقق من النسخة الاحتياطية")
    return target

def validate_backup(source):
    source=Path(source)
    if not source.exists(): return {"ok":False,"reason":"الملف غير موجود"}
    try:
        con=sqlite3.connect(str(source))
        integrity=con.execute("PRAGMA integrity_check").fetchone()[0]
        tables={r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        con.close()
        required={"children","lessons","words","progress"}
        return {"ok":integrity=="ok" and required.issubset(tables),"integrity":integrity,"tables":len(tables)}
    except Exception as exc: return {"ok":False,"reason":str(exc)}

def restore_database_safe(source):
    source=Path(source); check=validate_backup(source)
    if not check["ok"]: raise ValueError("النسخة الاحتياطية غير صالحة")
    if source.resolve()==DB_PATH.resolve(): raise ValueError("اختر ملفاً مختلفاً عن قاعدة البيانات الحالية")
    emergency=backup_database_safe(BACKUP_DIR/f"before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db") if DB_PATH.exists() else None
    engine.dispose()
    src=sqlite3.connect(str(source)); dst=sqlite3.connect(str(DB_PATH))
    try: src.backup(dst); dst.commit()
    finally: dst.close(); src.close()
    init_db()
    return {"database":DB_PATH,"emergency":emergency,"validation":check}
