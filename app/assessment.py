from sqlalchemy import select
from app.database import SessionLocal
from app.models import TestResult

def evaluate(answers, total):
    if total <= 0: return 0
    return round(max(0, min(100, sum(bool(x) for x in answers) / total * 100)), 2)

def save_result(child_id, language, skill, score):
    with SessionLocal() as s:
        r=TestResult(child_id=child_id,language=language,skill=skill,score=score)
        s.add(r); s.commit(); s.refresh(r); return r.id
