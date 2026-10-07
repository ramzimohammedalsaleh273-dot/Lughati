import shutil
from datetime import datetime
from app.config import DATA_DIR,BACKUP_DIR

def backup_database():
    src=DATA_DIR/"lughati.db"
    if not src.exists(): return None
    dst=BACKUP_DIR/f"lughati_{datetime.now():%Y%m%d_%H%M%S}.db"
    shutil.copy2(src,dst); return dst
