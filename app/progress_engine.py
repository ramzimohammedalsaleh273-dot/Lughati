"""محرك تقدم موحد يربط الدروس والمهارات والمراجعة والاختبارات."""
from sqlalchemy import select,func
from app.database import SessionLocal
from app.models import Progress,Lesson,TestResult,ReviewItem,Child,DailyPlan
from app.mastery import curriculum_progress
from app.skill_engine import report

def snapshot(child_id,language):
    levels=curriculum_progress(child_id,language)
    skills=report(child_id,language)
    with SessionLocal() as s:
        lessons=s.scalar(select(func.count()).select_from(Lesson).where(Lesson.language==language)) or 0
        completed=s.scalar(select(func.count()).select_from(Progress).join(Lesson,Lesson.id==Progress.lesson_id).where(Progress.child_id==child_id,Lesson.language==language)) or 0
        reviews=s.scalar(select(func.count()).select_from(ReviewItem).where(ReviewItem.child_id==child_id)) or 0
        tests=s.scalar(select(func.count()).select_from(TestResult).where(TestResult.child_id==child_id,TestResult.language==language)) or 0
    mastered=sum(x["mastered"] for x in levels)
    return {"lessons":lessons,"completed":completed,"mastered":mastered,"tests":tests,"review_items":reviews,"completion":round(completed/lessons*100,1) if lessons else 0,"mastery":round(mastered/lessons*100,1) if lessons else 0,"skills":skills}

def all_children():
    with SessionLocal() as s:return list(s.scalars(select(Child).order_by(Child.id)).all())
