from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA_DIR=ROOT/"data"; MEDIA_DIR=ROOT/"media"; BACKUP_DIR=ROOT/"backups"
for p in (DATA_DIR,MEDIA_DIR,BACKUP_DIR): p.mkdir(parents=True,exist_ok=True)
OFFLINE_FIRST=True
INTERNET_REQUIRED=False
APP_VERSION="1.0.0"
