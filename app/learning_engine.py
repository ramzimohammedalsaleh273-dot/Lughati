"""محرك التعلم المركزي للدفعة الأولى: الإتقان، التدرج، المهارات، والمراجعة."""
from dataclasses import dataclass
from sqlalchemy import select,func
from app.database import SessionLocal
from app.models import Lesson,Progress,TestResult,ReviewItem,Word,Child
from app.review import schedule

SKILLS=("listening","speaking","reading","writing","vocabulary","grammar")
MASTERY_THRESHOLD=80.0

@dataclass(frozen=True)
class LevelGate:
    level:int
    complete:bool
    mastery:float
    ready:bool

def lesson_score(child_id,lesson_id):
    with SessionLocal() as s:
        p=s.scalar(select(Progress).where(Progress.child_id==child_id,Progress.lesson_id==lesson_id))
        return float(p.score) if p else 0.0

def lesson_mastered(child_id,lesson_id):
    return lesson_score(child_id,lesson_id)>=MASTERY_THRESHOLD

def level_gate(child_id,language,level):
    with SessionLocal() as s:
        lessons=list(s.scalars(select(Lesson).where(Lesson.language==language,Lesson.level==level)).all())
        if not lessons:return LevelGate(level,False,0.0,False)
        ids=[x.id for x in lessons]
        rows=list(s.scalars(select(Progress).where(Progress.child_id==child_id,Progress.lesson_id.in_(ids))).all())
    by={x.lesson_id:x for x in rows}
    scores=[float(by[x.id].score) for x in lessons if x.id in by]
    mastered=sum(1 for x in lessons if x.id in by and x.mastered)
    avg=round(sum(scores)/len(scores),1) if scores else 0.0
    complete=len(rows)==len(lessons)
    return LevelGate(level,complete,avg,complete and mastered==len(lessons) and avg>=MASTERY_THRESHOLD)

def gates(child_id,language):
    return [level_gate(child_id,language,level) for level in range(13)]

def current_level(child_id,language):
    for gate in gates(child_id,language):
        if not gate.ready:return gate.level
    return 12

def skill_scores(child_id,language):
    with SessionLocal() as s:
        rows=list(s.scalars(select(TestResult).where(TestResult.child_id==child_id,TestResult.language==language)).all())
    out={}
    for skill in SKILLS:
        vals=[float(x.score) for x in rows if x.skill==skill]
        out[skill]=round(sum(vals)/len(vals),1) if vals else 0.0
    return out

def weakest_skills(child_id,language,limit=2):
    scores=skill_scores(child_id,language)
    return sorted(scores,key=lambda k:scores[k])[:max(1,int(limit))]

def ensure_review_items(child_id,language,level=0):
    with SessionLocal() as s:
        words=list(s.scalars(select(Word).where(Word.language==language,Word.level<=level).order_by(Word.level,Word.id)).all())
        existing={x.word_id for x in s.scalars(select(ReviewItem).where(ReviewItem.child_id==child_id)).all()}
        added=0
        for word in words:
            if word.id not in existing:
                s.add(ReviewItem(child_id=child_id,word_id=word.id))
                added+=1
        s.commit()
        return added

def record_word_review(child_id,word_id,quality):
    schedule(child_id,word_id,quality)
    return True

def learning_snapshot(child_id,language):
    gs=gates(child_id,language)
    scores=skill_scores(child_id,language)
    with SessionLocal() as s:
        lessons=s.scalar(select(func.count()).select_from(Lesson).where(Lesson.language==language)) or 0
        done=s.scalar(select(func.count()).select_from(Progress).join(Lesson,Lesson.id==Progress.lesson_id).where(Progress.child_id==child_id,Lesson.language==language)) or 0
        mastered=s.scalar(select(func.count()).select_from(Progress).join(Lesson,Lesson.id==Progress.lesson_id).where(Progress.child_id==child_id,Lesson.language==language,Progress.mastered==True)) or 0
    return {
        "current_level":current_level(child_id,language),
        "lessons":lessons,
        "completed":done,
        "mastered":mastered,
        "completion":round(done/lessons*100,1) if lessons else 0.0,
        "mastery":round(mastered/lessons*100,1) if lessons else 0.0,
        "skills":scores,
        "weakest":weakest_skills(child_id,language),
        "levels_ready":sum(1 for x in gs if x.ready),
    }
