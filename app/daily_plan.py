from dataclasses import dataclass
from datetime import date
from sqlalchemy import select
from app.database import SessionLocal
from app.models import DailyPlan, Lesson, ReviewItem, Word, Progress

@dataclass
class PlanTask:
    kind: str
    title: str
    ref_id: int | None = None
    minutes: int = 5
    done: bool = False

def build_plan(child_id:int, language:str="ar", minutes:int=20):
    tasks=[]
    with SessionLocal() as s:
        lesson= s.scalar(select(Lesson).where(Lesson.language==language).order_by(Lesson.level,Lesson.id))
        if lesson:
            p=s.scalar(select(Progress).where(Progress.child_id==child_id,Progress.lesson_id==lesson.id))
            if not p or not p.mastered: tasks.append(PlanTask("lesson",f"درس: {lesson.title}",lesson.id,8))
        due=list(s.scalars(select(ReviewItem).where(ReviewItem.child_id==child_id).order_by(ReviewItem.next_review).limit(5)).all())
        for item in due:
            w=s.get(Word,item.word_id)
            if w: tasks.append(PlanTask("review",f"مراجعة: {w.text}",w.id,4))
    if len(tasks)<3: tasks.append(PlanTask("test","اختبار قصير",None,5))
    total=0; result=[]
    for t in tasks:
        if total+t.minutes>minutes and result: continue
        result.append(t); total+=t.minutes
    return result

def get_or_create_plan(child_id:int,language:str="ar",minutes:int=20):
    today=date.today().isoformat()
    with SessionLocal() as s:
        p=s.scalar(select(DailyPlan).where(DailyPlan.child_id==child_id,DailyPlan.language==language,DailyPlan.date==today))
        if not p:
            p=DailyPlan(child_id=child_id,language=language,date=today,minutes=minutes,completed=False); s.add(p); s.commit()
        return p
