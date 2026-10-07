from pathlib import Path
from app.database import init_db
from app.seed import seed_content
from app.validation import full_check
from app.settings_service import ensure_defaults
from app.content_exchange import export_content,import_content
from app.backup_manager import backup_database_safe,validate_backup

def test_final_readiness(tmp_path):
    init_db(); seed_content()
    check=full_check()
    assert check["ok"], check
    settings=ensure_defaults()
    assert settings["language"]=="ar"
    backup=backup_database_safe(tmp_path/"final_backup.db")
    assert validate_backup(backup)["ok"]
    pack=export_content(tmp_path/"content.lughati")
    assert pack.exists() and pack.stat().st_size>0
    counts=import_content(pack)
    assert all(v>=0 for v in counts.values())

def test_required_project_surfaces():
    required=["README.md","main.py","app/database.py","app/models.py","app/ui/main_window.py","tests/test_final_readiness.py"]
    assert all(Path(p).exists() for p in required)
