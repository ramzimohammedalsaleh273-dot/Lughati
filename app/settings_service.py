from sqlalchemy import select
from app.database import SessionLocal
from app.models import UserSetting

def get_setting(key, default=None):
    with SessionLocal() as s:
        row=s.scalar(select(UserSetting).where(UserSetting.key==key))
        return row.value if row else default

def set_setting(key,value):
    with SessionLocal() as s:
        row=s.scalar(select(UserSetting).where(UserSetting.key==key))
        if not row:
            row=UserSetting(key=key); s.add(row)
        row.value=str(value); s.commit()
