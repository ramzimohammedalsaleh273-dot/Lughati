from datetime import datetime, timedelta
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Child, Lesson, Word, Progress, TestResult, ReviewItem, Story, Question, DailyPlan

def get_child():
    with SessionLocal() as s: return s.scalar(select(Child).order_by(Child.id))

def lessons(language=None, level=None):
    with SessionLocal() as s:
        q=select(Lesson).order_by(Lesson.level,Lesson.id)
        if language: q=q.where(Lesson.language==language)
        if level is not None: q=q.where(Lesson.level==level)
        return list(s.scalars(q).all())

def words(language=None, level=None, query=None):
    with SessionLocal() as s:
        q=select(Word).order_by(Word.level,Word.id)
        if language: q=q.where(Word.language==language)
        if level is not None: q=q.where(Word.level==level)
        if query: q=q.where(Word.text.contains(query) | Word.meaning.contains(query))
        return list(s.scalars(q).all())

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


def stories(language=None, level=None):
    with SessionLocal() as s:
        q=select(Story).order_by(Story.language,Story.level,Story.id)
        if language: q=q.where(Story.language==language)
        if level is not None: q=q.where(Story.level==level)
        return list(s.scalars(q).all())

def questions(language=None, level=None, skill=None):
    with SessionLocal() as s:
        q=select(Question).order_by(Question.level,Question.id)
        if language: q=q.where(Question.language==language)
        if level is not None: q=q.where(Question.level==level)
        if skill: q=q.where(Question.skill==skill)
        return list(s.scalars(q).all())

def search_words(language, query_text):
    q=query_text.strip()
    if not q: return words(language)
    with SessionLocal() as s:
        stmt=select(Word).where(Word.language==language).where(Word.text.contains(q) | Word.meaning.contains(q)).order_by(Word.level,Word.id)
        return list(s.scalars(stmt).all())


def create_daily_plan(child_id,language="ar",minutes=20):
    today=datetime.now().date().isoformat()
    with SessionLocal() as s:
        p=s.scalar(select(DailyPlan).where(DailyPlan.child_id==child_id,DailyPlan.date==today,DailyPlan.language==language))
        if not p:
            p=DailyPlan(child_id=child_id,date=today,language=language,minutes=minutes); s.add(p); s.commit()
        return p
