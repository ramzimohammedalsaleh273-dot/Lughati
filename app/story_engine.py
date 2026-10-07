import json
from dataclasses import dataclass

@dataclass
class StorySession:
    story_id:int
    language:str
    level:int
    title:str
    body:str
    questions:list

def parse_questions(raw):
    try:
        data=json.loads(raw or "[]")
        return data if isinstance(data,list) else []
    except Exception:
        return []

def build_session(story):
    return StorySession(story.id,story.language,story.level,story.title,story.body,parse_questions(story.questions))

def comprehension_score(story,answers):
    qs=parse_questions(story.questions)
    if not qs:return 0.0
    correct=0
    for q,a in zip(qs,answers):
        if str(a).strip().casefold()==str(q.get("answer","")).strip().casefold():correct+=1
    return round(correct/len(qs)*100,1)
