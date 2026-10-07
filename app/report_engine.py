"""محرك تقارير شامل لولي الأمر."""
from datetime import datetime, timedelta
from sqlalchemy import select, func
from app.database import SessionLocal
from app.models import Child, Progress, TestResult, DailyPlan, ReviewItem, AssessmentAttempt, Recording
from app.progress_engine import snapshot

def child_summary(child_id, language=None):
    with SessionLocal() as s:
        c=s.get(Child,int(child_id))
        if not c: raise ValueError("الطفل غير موجود")
        languages=[language] if language else ["ar","en"]
        result={"child":{"id":c.id,"name":c.name,"age":c.age},"languages":{}}
        for lang in languages: result["languages"][lang]=snapshot(c.id,lang)
        result["totals"]={
            "tests":s.scalar(select(func.count()).select_from(TestResult).where(TestResult.child_id==c.id)) or 0,
            "reviews":s.scalar(select(func.count()).select_from(ReviewItem).where(ReviewItem.child_id==c.id)) or 0,
            "completed_plans":s.scalar(select(func.count()).select_from(DailyPlan).where(DailyPlan.child_id==c.id,DailyPlan.completed.is_(True))) or 0,
            "recordings":s.scalar(select(func.count()).select_from(Recording).where(Recording.child_id==c.id)) or 0,
            "assessments":s.scalar(select(func.count()).select_from(AssessmentAttempt).where(AssessmentAttempt.child_id==c.id)) or 0,
        }
        return result

def activity_summary(child_id, days=30):
    cutoff=datetime.utcnow()-timedelta(days=int(days))
    with SessionLocal() as s:
        return {
            "days":int(days),
            "lessons":s.scalar(select(func.count()).select_from(Progress).where(Progress.child_id==child_id,Progress.updated_at>=cutoff)) or 0,
            "tests":s.scalar(select(func.count()).select_from(TestResult).where(TestResult.child_id==child_id,TestResult.created_at>=cutoff)) or 0,
            "plans":s.scalar(select(func.count()).select_from(DailyPlan).where(DailyPlan.child_id==child_id,DailyPlan.completed.is_(True),DailyPlan.date>=cutoff.date().isoformat())) or 0,
        }

def skill_report(child_id, language):
    return {k:round(float(v),1) for k,v in child_summary(child_id,language)["languages"][language]["skills"].items()}
