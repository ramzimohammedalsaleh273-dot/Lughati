from pathlib import Path
from sqlalchemy import select
from app.database import SessionLocal
from app.models import MediaAsset

KINDS=("audio","video","story_audio","story_video","lesson_audio","lesson_video")

def assets(language=None,level=None,kind=None,offline_only=False):
    with SessionLocal() as s:
        q=select(MediaAsset).order_by(MediaAsset.language,MediaAsset.level,MediaAsset.id)
        if language:q=q.where(MediaAsset.language==language)
        if level is not None:q=q.where(MediaAsset.level==level)
        if kind:q=q.where(MediaAsset.kind==kind)
        if offline_only:q=q.where(MediaAsset.offline_ready==True)
        return list(s.scalars(q).all())

def register_asset(language,level,kind,title,path="",source="",offline_ready=False):
    path=str(Path(path)) if path else ""
    with SessionLocal() as s:
        row=MediaAsset(language=language,level=level,kind=kind,title=title,path=path,source=source,offline_ready=offline_ready)
        s.add(row); s.commit(); return row.id

def mark_offline(asset_id,ready=True):
    with SessionLocal() as s:
        row=s.get(MediaAsset,asset_id)
        if not row:return False
        row.offline_ready=bool(ready); s.commit(); return True
