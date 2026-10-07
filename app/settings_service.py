"""إعدادات التطبيق المخزنة محلياً."""
from app.database import SessionLocal
from app.models import UserSetting

DEFAULTS={"language":"ar","theme":"فاتح","daily_minutes":"20","content_version":"1","audio_enabled":"true","video_autoplay":"false","parent_lock":"true","sync_endpoint":"","sync_token":""}

def get(key, default=None):
    with SessionLocal() as s:
        row=s.query(UserSetting).filter_by(key=str(key)).first()
        return row.value if row else default

def set(key,value):
    with SessionLocal() as s:
        row=s.query(UserSetting).filter_by(key=str(key)).first()
        if not row: row=UserSetting(key=str(key)); s.add(row)
        row.value=str(value); s.commit(); return row.value

def all_settings():
    with SessionLocal() as s:
        return {x.key:x.value for x in s.query(UserSetting).order_by(UserSetting.key).all()}

def ensure_defaults():
    with SessionLocal() as s:
        for key,value in DEFAULTS.items():
            row=s.query(UserSetting).filter_by(key=key).first()
            if not row: s.add(UserSetting(key=key,value=value))
        s.commit()
    return all_settings()
