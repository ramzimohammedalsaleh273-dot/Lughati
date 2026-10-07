from dataclasses import dataclass
from datetime import date
import json
from sqlalchemy import select
from app.database import SessionLocal
from app.models import DailyPlan, Lesson, ReviewItem, Word, Progress

@dataclass
class PlanTask:
    kind:str
    title:str
    ref_id:int|None=None
    minutes:int=5
    done:bool=False

def build_plan(child_id:int,language:str="ar",minutes:int=20):
    tasks=[]
    with SessionLocal() as s:
        lessons=list(s.scalars(select(Lesson).where(Lesson.language==language).order_by(Lesson.level,Lesson.id)).all())
        progress={p.lesson_id:p for p in s.scalars(select(Progress).where(Progress.child_id==child_id)).all()}
        for lesson in lessons:
            p=progress.get(lesson.id)
            if not p or not p.mastered:
                tasks.append(PlanTask("lesson",f"درس: {lesson.title}",lesson.id,8)); break
        due=list(s.scalars(select(ReviewItem).where(ReviewItem.child_id==child_id).order_by(ReviewItem.next_review).limit(5)).all())
        for item in due:
            w=s.get(Word,item.word_id)
            if w: tasks.append(PlanTask("review",f"مراجعة: {w.text}",w.id,4))
    if len(tasks)<3: tasks.append(PlanTask("test","اختبار قصير",None,5))
    result=[]; total=0
    for task in tasks:
        if total+task.minutes>minutes and result: continue
        result.append(task); total+=task.minutes
    return result

def get_or_create_plan(child_id:int,language:str="ar",minutes:int=20):
    today=date.today().isoformat(); tasks=build_plan(child_id,language,minutes)
    payload=[{"kind":x.kind,"title":x.title,"ref_id":x.ref_id,"minutes":x.minutes,"done":x.done} for x in tasks]
    with SessionLocal() as s:
        p=s.scalar(select(DailyPlan).where(DailyPlan.child_id==child_id,DailyPlan.language==language,DailyPlan.date==today))
        if not p:
            p=DailyPlan(child_id=child_id,language=language,date=today,minutes=minutes,completed=False,tasks=json.dumps(payload,ensure_ascii=False)); s.add(p); s.commit()
        elif not p.tasks or p.minutes!=minutes:
            p.minutes=minutes; p.tasks=json.dumps(payload,ensure_ascii=False); s.commit()
        return p
