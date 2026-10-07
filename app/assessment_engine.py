import json
from dataclasses import dataclass
from app.assessment import load_questions, grade, options

@dataclass
class ItemResult:
    question_id:int
    correct:bool
    answer:str

def normalize_answer(value):
    return " ".join(str(value or "").strip().casefold().split())

def grade_item(question, answer):
    if getattr(question,"skill","")=="speaking":
        return bool(str(answer).strip())
    return grade(question,answer)

def prepare(question):
    kind="mcq"
    try:
        payload=json.loads(question.options or "[]")
        if isinstance(payload,dict): kind=payload.get("type","mcq")
    except Exception:
        payload=[]
    return {"type":kind,"prompt":question.prompt,"options":options(question),"answer":question.answer}

def score_items(items):
    correct=sum(1 for x in items if x.correct)
    return round(correct/len(items)*100,1) if items else 0.0
