import json
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Lesson,Word,Story,Question

TABLES={"lessons":Lesson,"words":Word,"stories":Story,"questions":Question}

def export_content(path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    payload={}
    with SessionLocal() as s:
        for name,model in TABLES.items():
            rows=s.scalars(select(model)).all()
            payload[name]=[{k:v for k,v in row.__dict__.items() if not k.startswith("_")} for row in rows]
    with ZipFile(path,"w",ZIP_DEFLATED) as z:
        z.writestr("manifest.json",json.dumps({"format":"lughati-content","version":1},ensure_ascii=False,indent=2))
        z.writestr("content.json",json.dumps(payload,ensure_ascii=False,default=str))
    return path

def import_content(path):
    path=Path(path)
    with ZipFile(path) as z:
        if z.read("manifest.json").decode("utf-8").strip()=="":
            raise ValueError("حزمة المحتوى غير صالحة")
        payload=json.loads(z.read("content.json").decode("utf-8"))
    counts={}
    with SessionLocal() as s:
        for name,model in TABLES.items():
            count=0
            for data in payload.get(name,[]):
                data={k:v for k,v in data.items() if k not in {"id","created_at","updated_at"}}
                if not data: continue
                s.add(model(**data)); count+=1
            counts[name]=count
        s.commit()
    return counts
