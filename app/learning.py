from sqlalchemy import select
from app.database import SessionLocal
from app.models import Lesson,Progress,Child,TestResult

def mastery(child_id,language=None):
 with SessionLocal() as s:
  q=select(Progress).where(Progress.child_id==child_id)
  rows=list(s.scalars(q)); return round(sum(p.score for p in rows)/len(rows),1) if rows else 0

def skill_report(child_id):
 with SessionLocal() as s:
  rows=list(s.scalars(select(TestResult).where(TestResult.child_id==child_id)))
  out={}
  for r in rows: out.setdefault(r.skill,[]).append(r.score)
  return {k:round(sum(v)/len(v),1) for k,v in out.items()}
