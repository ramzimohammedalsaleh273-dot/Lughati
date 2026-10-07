from pathlib import Path
from app.database import init_db
from app.seed import seed_content
from app.child_manager import create_child,update_child,delete_child
from app.settings_service import ensure_defaults,set
from app.report_engine import child_summary,activity_summary,skill_report
from app.backup_manager import backup_database_safe,validate_backup

def test_children_and_reports():
    init_db(); seed_content()
    cid=create_child("اختبار الدفعة الثالثة",9)
    update_child(cid,name="اختبار محدث",age=10)
    r=child_summary(cid); assert r["child"]["name"]=="اختبار محدث"; assert "ar" in r["languages"]
    assert activity_summary(cid)["lessons"]==0
    assert isinstance(skill_report(cid,"ar"),dict)
    assert delete_child(cid)

def test_settings_defaults():
    init_db(); ensure_defaults(); assert set("daily_minutes","30")=="30"

def test_safe_backup(tmp_path):
    init_db(); seed_content()
    p=backup_database_safe(Path(tmp_path)/"test.db")
    assert validate_backup(p)["ok"] is True
