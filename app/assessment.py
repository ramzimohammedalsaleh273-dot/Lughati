from __future__ import annotations
from dataclasses import dataclass
import json
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Question, TestResult

@dataclass
class AssessmentResult:
    total:int; correct:int; score:float; language:str; skill:str; level:int

def load_questions(language,level=None,skill=None,limit=20):
    with SessionLocal() as s:
        q=select(Question).where(Question.language==language)
        if level is not None: q=q.where(Question.level==level)
        if skill: q=q.where(Question.skill==skill)
        return list(s.scalars(q.order_by(Question.level,Question.id)).all())[:max(1,limit)]

def payload(question):
    try: return json.loads(question.options or "[]")
    except (TypeError,ValueError): return []

def question_type(question):
    p=payload(question)
    return p.get("type","mcq") if isinstance(p,dict) else "mcq"

def options(question):
    p=payload(question)
    if isinstance(p,dict): return [str(x) for x in p.get("options",[])]
    return [str(x) for x in p]

def grade(question,answer):
    if question_type(question)=="order":
        expected=str(question.answer).strip().replace(" ","")
        actual=str(answer).strip().replace(" ","")
        return expected.casefold()==actual.casefold()
    return str(answer).strip().casefold()==str(question.answer).strip().casefold()

def finish(child_id,language,skill,level,total,correct):
    score=round((correct/total)*100,1) if total else 0.0
    with SessionLocal() as s:
        s.add(TestResult(child_id=child_id,language=language,skill=skill,score=score)); s.commit()
    return AssessmentResult(total,correct,score,language,skill,level)

def placement_level(results):
    if not results:return 0
    return min(12,max(0,int(sum(x.score for x in results)//10)*2))
