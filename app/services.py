from datetime import datetime, timedelta
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Child, Lesson, Word, Progress, TestResult, ReviewItem

def get_child():
    with SessionLocal() as s: return s.scalar(select(Child).order_by(Child.id))

def lessons(language):
    with SessionLocal() as s: return list(s.scalars(select(Lesson).where(Lesson.language==language).order_by(Lesson.level)))

def words(language):
    with SessionLocal() as s: return list(s.scalars(select(Word).where(Word.language==language).order_by(Word.id)))

def save_lesson(child_id, lesson_id, score):
    with SessionLocal() as s:
        p=s.scalar(select(Progress).where(Progress.child_id==child_id,Progress.lesson_id==lesson_id))
        if not p: p=Progress(child_id=child_id,lesson_id=lesson_id); s.add(p)
        p.score=max(p.score,score); p.mastered=p.score>=80; p.updated_at=datetime.utcnow(); s.commit()

def save_test(child_id,language,skill,score):
    with SessionLocal() as s: s.add(TestResult(child_id=child_id,language=language,skill=skill,score=score)); s.commit()

def dashboard(child_id):
    with SessionLocal() as s:
        ps=list(s.scalars(select(Progress).where(Progress.child_id==child_id)))
        ts=list(s.scalars(select(TestResult).where(TestResult.child_id==child_id)))
        return len(ps), sum(1 for p in ps if p.mastered), round(sum(t.score for t in ts)/len(ts),1) if ts else 0
