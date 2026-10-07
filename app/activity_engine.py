"""تسلسل تنفيذ الدرس: نشاط، تحقق، نتيجة."""
from dataclasses import dataclass
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Activity,Lesson,Progress
from app.services import save_lesson

@dataclass
class ActivityState:
    lesson_id:int
    index:int
    total:int
    done:bool

def activities(lesson_id):
    with SessionLocal() as s:
        return list(s.scalars(select(Activity).where(Activity.lesson_id==lesson_id).order_by(Activity.order_no,Activity.id)).all())

def state(lesson_id,index=0):
    items=activities(lesson_id)
    return ActivityState(lesson_id,index,len(items),index>=len(items))

def finish_lesson(child_id,lesson_id,score):
    save_lesson(child_id,lesson_id,max(0,min(100,float(score))))
    return state(lesson_id)
