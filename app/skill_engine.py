"""قياس المهارات الست من نتائج الاختبارات والأنشطة."""
from dataclasses import dataclass
from app.learning import skill_report
from app.mastery import curriculum_progress

SKILLS=("listening","speaking","reading","writing","vocabulary","grammar")

@dataclass
class SkillStatus:
    skill:str
    score:float
    level:str
    weak:bool

def report(child_id,language):
    raw=skill_report(child_id,language)
    return [SkillStatus(s,float(raw.get(s,0)),("قوي" if raw.get(s,0)>=80 else "متوسط" if raw.get(s,0)>=60 else "يحتاج تدريب"),float(raw.get(s,0))<60) for s in SKILLS]

def weakest(child_id,language,limit=2):
    return sorted(report(child_id,language),key=lambda x:x.score)[:max(1,int(limit))]

def readiness(child_id,language):
    rows=curriculum_progress(child_id,language)
    current=next((x for x in rows if not x["ready_for_next"]),rows[-1] if rows else None)
    skills=report(child_id,language)
    avg=round(sum(x.score for x in skills)/len(skills),1) if skills else 0
    return {"current_level":current["level"] if current else 12,"skill_average":avg,"weakest":[x.skill for x in weakest(child_id,language)],"ready":bool(current and current["ready_for_next"])}
