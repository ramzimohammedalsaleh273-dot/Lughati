from collections import defaultdict
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Progress,Lesson,TestResult

def snapshot(child_id):
    with SessionLocal() as s:
        ps=list(s.execute(select(Progress,Lesson).join(Lesson,Progress.lesson_id==Lesson.id).where(Progress.child_id==child_id)).all())
        ts=list(s.scalars(select(TestResult).where(TestResult.child_id==child_id)).all())
    by_language=defaultdict(list)
    for p,l in ps: by_language[l.language].append(p.score)
    by_skill=defaultdict(list)
    for t in ts: by_skill[t.skill].append(t.score)
    return {"languages":{k:round(sum(v)/len(v),1) for k,v in by_language.items()},"skills":{k:round(sum(v)/len(v),1) for k,v in by_skill.items()},"lessons":len(ps),"mastered":sum(1 for p,_ in ps if p.mastered)}