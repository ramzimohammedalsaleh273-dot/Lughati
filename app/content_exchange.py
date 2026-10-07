import json, hashlib
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Lesson,Word,Story,Question

TABLES={"lessons":Lesson,"words":Word,"stories":Story,"questions":Question}
KEYS={"lessons":("language","level","title"),"words":("language","text"),"stories":("language","level","title"),"questions":("language","level","prompt")}

def _payload():
    payload={}
    with SessionLocal() as s:
        for name,model in TABLES.items():
            rows=s.scalars(select(model)).all()
            payload[name]=[{k:v for k,v in row.__dict__.items() if not k.startswith("_") and k not in {"created_at","updated_at","id"}} for row in rows]
    return payload

def export_content(path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    payload=_payload(); raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,default=str).encode()
    manifest={"format":"lughati-content","version":3,"languages":["ar","en"],"offline":True,"sha256":hashlib.sha256(raw).hexdigest(),"counts":{k:len(v) for k,v in payload.items()}}
    with ZipFile(path,"w",ZIP_DEFLATED) as z:
        z.writestr("manifest.json",json.dumps(manifest,ensure_ascii=False,indent=2))
        z.writestr("content.json",raw)
    return path

def import_content(path):
    path=Path(path)
    with ZipFile(path) as z:
        names=set(z.namelist())
        if not {"manifest.json","content.json"}.issubset(names): raise ValueError("حزمة المحتوى ناقصة")
        manifest=json.loads(z.read("manifest.json").decode()); raw=z.read("content.json")
        if manifest.get("format")!="lughati-content": raise ValueError("حزمة المحتوى غير صالحة")
        expected=manifest.get("sha256")
        if expected and hashlib.sha256(raw).hexdigest()!=expected: raise ValueError("الحزمة تالفة أو تم تعديلها")
        payload=json.loads(raw.decode("utf-8"))
    counts={name:0 for name in TABLES}
    with SessionLocal() as s:
        for name,model in TABLES.items():
            for rawrow in payload.get(name,[]):
                data={k:v for k,v in rawrow.items() if k not in {"id","created_at","updated_at"}}
                if not data: continue
                existing=s.scalar(select(model).filter_by(**{k:data.get(k) for k in KEYS[name]}))
                if existing:
                    for k,v in data.items(): setattr(existing,k,v)
                else: s.add(model(**data))
                counts[name]+=1
        s.commit()
    return counts
