from sqlalchemy import select,func
from app.database import SessionLocal
from app.models import Lesson,Progress,TestResult,Activity

def mastery(child_id,language=None):
    with SessionLocal() as s:
        q=select(Progress,Lesson).join(Lesson,Lesson.id==Progress.lesson_id).where(Progress.child_id==child_id)
        if language:q=q.where(Lesson.language==language)
        rows=list(s.execute(q).all())
    return round(sum(p.score for p,_ in rows)/len(rows),1) if rows else 0

def skill_report(child_id,language=None):
    with SessionLocal() as s:
        q=select(TestResult).where(TestResult.child_id==child_id)
        if language:q=q.where(TestResult.language==language)
        rows=list(s.scalars(q).all())
    out={}
    for r in rows:out.setdefault(r.skill,[]).append(float(r.score))
    return {k:round(sum(v)/len(v),1) for k,v in out.items()}

def level_status(child_id,language):
    with SessionLocal() as s:
        lessons=list(s.scalars(select(Lesson).where(Lesson.language==language).order_by(Lesson.level,Lesson.id)).all())
        progress={p.lesson_id:p for p in s.scalars(select(Progress).where(Progress.child_id==child_id)).all()}
    return [{"level":x.level,"title":x.title,"score":progress[x.id].score if x.id in progress else 0,"mastered":bool(progress.get(x.id) and progress.get(x.id).mastered)} for x in lessons]

def lesson_completion(child_id,language):
    with SessionLocal() as s:
        total=s.scalar(select(func.count()).select_from(Lesson).where(Lesson.language==language)) or 0
        done=s.scalar(select(func.count()).select_from(Progress).join(Lesson,Lesson.id==Progress.lesson_id).where(Progress.child_id==child_id,Lesson.language==language)) or 0
    return {"total":total,"done":done,"percent":round(done/total*100,1) if total else 0}

def activity_count(lesson_id):
    with SessionLocal() as s:return s.scalar(select(func.count()).select_from(Activity).where(Activity.lesson_id==lesson_id)) or 0
