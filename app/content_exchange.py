import json
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Lesson,Word,Story,Question

TABLES={"lessons":Lesson,"words":Word,"stories":Story,"questions":Question}
KEYS={"lessons":("language","level","title"),"words":("language","text"),"stories":("language","level","title"),"questions":("language","level","prompt")}

def export_content(path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    payload={}
    with SessionLocal() as s:
        for name,model in TABLES.items():
            rows=s.scalars(select(model)).all()
            payload[name]=[{k:v for k,v in row.__dict__.items() if not k.startswith("_")} for row in rows]
    manifest={"format":"lughati-content","version":2,"languages":["ar","en"],"offline":True}
    with ZipFile(path,"w",ZIP_DEFLATED) as z:
        z.writestr("manifest.json",json.dumps(manifest,ensure_ascii=False,indent=2))
        z.writestr("content.json",json.dumps(payload,ensure_ascii=False,default=str))
    return path

def import_content(path):
    path=Path(path)
    with ZipFile(path) as z:
        manifest=json.loads(z.read("manifest.json").decode("utf-8"))
        if manifest.get("format")!="lughati-content":raise ValueError("حزمة المحتوى غير صالحة")
        payload=json.loads(z.read("content.json").decode("utf-8"))
    counts={name:0 for name in TABLES}
    with SessionLocal() as s:
        for name,model in TABLES.items():
            keys=KEYS[name]
            for raw in payload.get(name,[]):
                data={k:v for k,v in raw.items() if k not in {"id","created_at","updated_at"}}
                if not data:continue
                filters={k:data.get(k) for k in keys}
                existing=s.scalar(select(model).filter_by(**filters))
                if existing:
                    for k,v in data.items():setattr(existing,k,v)
                else:
                    s.add(model(**data))
                counts[name]+=1
        s.commit()
    return counts
