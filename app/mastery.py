from sqlalchemy import select, func
from app.database import SessionLocal
from app.models import Progress, Lesson, TestResult

def lesson_mastery(score):
    return float(score) >= 80

def level_summary(child_id, language, level):
    with SessionLocal() as s:
        lessons=list(s.scalars(select(Lesson).where(Lesson.language==language,Lesson.level==level)).all())
        ids=[x.id for x in lessons]
        rows=list(s.scalars(select(Progress).where(Progress.child_id==child_id,Progress.lesson_id.in_(ids))).all()) if ids else []
    by={x.lesson_id:x for x in rows}
    scores=[by[x.id].score for x in lessons if x.id in by]
    mastered=sum(1 for x in lessons if x.id in by and x.mastered)
    average=round(sum(scores)/len(scores),1) if scores else 0
    complete=len(rows)>=len(lessons) if lessons else False
    return {"language":language,"level":level,"lessons":len(lessons),"completed":len(rows),"mastered":mastered,"average":average,"complete":complete,"ready_for_next":complete and average>=80}

def curriculum_progress(child_id, language):
    return [level_summary(child_id,language,lvl) for lvl in range(13)]

def recommended_next_level(child_id, language):
    for row in curriculum_progress(child_id,language):
        if not row["ready_for_next"]:
            return row["level"]
    return 12

def skill_averages(child_id, language=None):
    with SessionLocal() as s:
        q=select(TestResult.skill,func.avg(TestResult.score)).where(TestResult.child_id==child_id)
        if language: q=q.where(TestResult.language==language)
        rows=s.execute(q.group_by(TestResult.skill)).all()
    return {skill:round(float(avg),1) for skill,avg in rows}
