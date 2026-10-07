import csv, json
from pathlib import Path
from app.database import SessionLocal
from app.models import Child, Progress, TestResult

def export_json(path):
    with SessionLocal() as s:
        children=s.scalars(Child).all(); progress=s.scalars(Progress).all(); tests=s.scalars(TestResult).all()
        data={"children":[{"id":x.id,"name":x.name,"age":x.age} for x in children],
              "progress":[{"child_id":x.child_id,"lesson_id":x.lesson_id,"score":x.score,"mastered":x.mastered} for x in progress],
              "tests":[{"child_id":x.child_id,"language":x.language,"skill":x.skill,"score":x.score} for x in tests]}
    Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
