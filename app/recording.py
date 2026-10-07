from pathlib import Path
from app.database import SessionLocal
from app.models import Recording

ROOT=Path("data/recordings")

def register_recording(child_id,language,prompt,path,duration=0,self_score=0):
    ROOT.mkdir(parents=True,exist_ok=True)
    path=Path(path)
    with SessionLocal() as s:
        r=Recording(child_id=child_id,language=language,prompt=prompt,path=str(path.resolve()),duration=float(duration),self_score=max(0,min(100,int(self_score))))
        s.add(r);s.commit();return r.id

def recordings(child_id,language=None):
    with SessionLocal() as s:
        q=s.query(Recording).filter_by(child_id=child_id)
        if language:q=q.filter_by(language=language)
        return list(q.order_by(Recording.id.desc()).all())

def delete_recording(recording_id,delete_file=False):
    with SessionLocal() as s:
        row=s.get(Recording,recording_id)
        if not row:return False
        path=Path(row.path)
        s.delete(row);s.commit()
    if delete_file and path.exists():
        try:path.unlink()
        except OSError:pass
    return True
