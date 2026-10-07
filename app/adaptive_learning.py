from app.learning_engine import skill_scores,weakest_skills,current_level
from app.review import due

def recommendations(child_id,language,limit=6):
    weak=weakest_skills(child_id,language,2)
    level=current_level(child_id,language)
    out=[{"kind":"skill","skill":x,"level":level,"reason":"مهارة تحتاج تدريباً"} for x in weak]
    due_items=due(child_id,limit=limit)
    for item,word in due_items:
        out.append({"kind":"review","word_id":word.id,"title":word.text,"reason":"مراجعة مستحقة"})
    return out[:max(1,int(limit))]

def plan_minutes(child_id,language,minutes=20):
    minutes=max(10,int(minutes))
    recs=recommendations(child_id,language,8)
    slots=[]; used=0
    for r in recs:
        cost=4 if r["kind"]=="review" else 6
        if used+cost>minutes and slots:break
        slots.append({**r,"minutes":cost}); used+=cost
    if not slots: slots=[{"kind":"lesson","level":current_level(child_id,language),"minutes":min(8,minutes),"reason":"الدرس التالي"}]
    return slots
