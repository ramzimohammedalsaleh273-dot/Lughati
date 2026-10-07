from pathlib import Path
from datetime import datetime
from app.database import SessionLocal
from app.models import Recording

ROOT=Path("data/recordings")

def register_recording(child_id, language, prompt, path, duration=0, self_score=0):
    ROOT.mkdir(parents=True,exist_ok=True)
    with SessionLocal() as s:
        r=Recording(child_id=child_id,language=language,prompt=prompt,path=str(path),duration=duration,self_score=self_score)
        s.add(r); s.commit(); return r.id

def recordings(child_id):
    with SessionLocal() as s:
        return list(s.query(Recording).filter_by(child_id=child_id).order_by(Recording.id.desc()).all())
