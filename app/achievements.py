from sqlalchemy import select
from app.database import SessionLocal
from app.models import Progress, TestResult

def summary(child_id):
    with SessionLocal() as s:
        lessons=s.scalars(select(Progress).where(Progress.child_id==child_id)).all()
        tests=s.scalars(select(TestResult).where(TestResult.child_id==child_id)).all()
    mastered=sum(1 for x in lessons if x.mastered)
    avg=round(sum(x.score for x in tests)/len(tests),1) if tests else 0
    return {"lessons_mastered":mastered,"tests":len(tests),"test_average":avg}
