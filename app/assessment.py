from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
import json
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Question, TestResult, AssessmentAttempt

@dataclass
class AssessmentResult:
    total:int
    correct:int
    score:float
    language:str
    skill:str
    level:int

def load_questions(language,level=None,skill=None,limit=20):
    with SessionLocal() as s:
        q=select(Question).where(Question.language==language)
        if level is not None:q=q.where(Question.level==level)
        if skill:q=q.where(Question.skill==skill)
        return list(s.scalars(q.order_by(Question.level,Question.id)).all())[:max(1,limit)]

def payload(question):
    try:return json.loads(question.options or "[]")
    except (TypeError,ValueError):return []

def question_type(question):
    p=payload(question)
    return p.get("type","mcq") if isinstance(p,dict) else "mcq"

def options(question):
    p=payload(question)
    if isinstance(p,dict):return [str(x) for x in p.get("options",[])]
    return [str(x) for x in p]

def normalize(value):
    return " ".join(str(value or "").strip().casefold().split())

def grade(question,answer):
    kind=question_type(question)
    if kind=="true_false":
        return normalize(answer)==normalize(question.answer)
    if kind=="order":
        return normalize(answer).replace(" ","")==normalize(question.answer).replace(" ","")
    if kind in ("writing","listening"):
        return normalize(answer)==normalize(question.answer)
    if kind=="speaking":
        return bool(normalize(answer))
    return normalize(answer)==normalize(question.answer)

def finish(child_id,language,skill,level,total,correct):
    score=round((correct/total)*100,1) if total else 0.0
    with SessionLocal() as s:
        s.add(TestResult(child_id=child_id,language=language,skill=skill,score=score))
        s.add(AssessmentAttempt(child_id=child_id,language=language,level=level,total=total,correct=correct,score=score,finished_at=datetime.utcnow()))
        s.commit()
    return AssessmentResult(total,correct,score,language,skill,level)

def placement_level(results):
    if not results:return 0
    average=sum(float(x.score) for x in results)/len(results)
    if average<40:return 0
    if average<50:return 2
    if average<60:return 4
    if average<70:return 6
    if average<80:return 8
    if average<90:return 10
    return 12
