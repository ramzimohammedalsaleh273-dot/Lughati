from datetime import datetime
from sqlalchemy import select,func
from app.database import SessionLocal
from app.models import Child,Lesson,Word,Progress,TestResult,ReviewItem,Story,Question,DailyPlan,Achievement,ChildAchievement
from app.state import child_id as session_child_id

def children():
    with SessionLocal() as s:return list(s.scalars(select(Child).order_by(Child.id)).all())
def get_child():
    wanted=session_child_id()
    with SessionLocal() as s:
        if wanted:
            child=s.get(Child,wanted)
            if child:return child
        return s.scalar(select(Child).order_by(Child.id))
def get_child_by_id(child_id):
    with SessionLocal() as s:return s.get(Child,int(child_id))
def lessons(language=None,level=None):
    with SessionLocal() as s:
        q=select(Lesson).order_by(Lesson.level,Lesson.id)
        if language:q=q.where(Lesson.language==language)
        if level is not None:q=q.where(Lesson.level==level)
        return list(s.scalars(q).all())
def words(language=None,level=None,query=None):
    with SessionLocal() as s:
        q=select(Word).order_by(Word.level,Word.id)
        if language:q=q.where(Word.language==language)
        if level is not None:q=q.where(Word.level==level)
        if query:q=q.where(Word.text.contains(query)|Word.meaning.contains(query))
        return list(s.scalars(q).all())
def save_lesson(child_id,lesson_id,score):
    with SessionLocal() as s:
        p=s.scalar(select(Progress).where(Progress.child_id==child_id,Progress.lesson_id==lesson_id))
        if not p:p=Progress(child_id=child_id,lesson_id=lesson_id);s.add(p)
        p.score=max(p.score,score);p.mastered=p.score>=80;p.updated_at=datetime.utcnow();s.commit()
    from app.sync import queue
    queue("progress",lesson_id,"upsert",{"child_id":child_id,"lesson_id":lesson_id,"score":score})
    auto_award(child_id)
def save_test(child_id,language,skill,score):
    with SessionLocal() as s:
        row=TestResult(child_id=child_id,language=language,skill=skill,score=score);s.add(row);s.commit();rid=row.id
    from app.sync import queue
    queue("test_result",rid,"create",{"child_id":child_id,"language":language,"skill":skill,"score":score})
    auto_award(child_id)
def dashboard(child_id):
    with SessionLocal() as s:
        ps=list(s.scalars(select(Progress).where(Progress.child_id==child_id)));ts=list(s.scalars(select(TestResult).where(TestResult.child_id==child_id)))
        return len(ps),sum(1 for p in ps if p.mastered),round(sum(t.score for t in ts)/len(ts),1) if ts else 0
def stories(language=None,level=None):
    with SessionLocal() as s:
        q=select(Story).order_by(Story.language,Story.level,Story.id)
        if language:q=q.where(Story.language==language)
        if level is not None:q=q.where(Story.level==level)
        return list(s.scalars(q).all())
def questions(language=None,level=None,skill=None):
    with SessionLocal() as s:
        q=select(Question).order_by(Question.level,Question.id)
        if language:q=q.where(Question.language==language)
        if level is not None:q=q.where(Question.level==level)
        if skill:q=q.where(Question.skill==skill)
        return list(s.scalars(q).all())
def search_words(language,query_text):return words(language,query=query_text.strip())
def create_daily_plan(child_id,language="ar",minutes=20):
    today=datetime.now().date().isoformat()
    with SessionLocal() as s:
        p=s.scalar(select(DailyPlan).where(DailyPlan.child_id==child_id,DailyPlan.date==today,DailyPlan.language==language))
        if not p:p=DailyPlan(child_id=child_id,date=today,language=language,minutes=minutes);s.add(p)
        else:p.minutes=minutes
        s.commit();return p
def complete_daily_plan(child_id,language):
    today=datetime.now().date().isoformat()
    with SessionLocal() as s:
        p=s.scalar(select(DailyPlan).where(DailyPlan.child_id==child_id,DailyPlan.date==today,DailyPlan.language==language))
        if p:p.completed=True;s.commit()
        return bool(p)
def progress_for(child_id,language=None):
    with SessionLocal() as s:
        q=select(Progress,Lesson).join(Lesson,Lesson.id==Progress.lesson_id).where(Progress.child_id==child_id)
        if language:q=q.where(Lesson.language==language)
        return list(s.execute(q).all())
def achievement_status(child_id):
    with SessionLocal() as s:
        all_items=list(s.scalars(select(Achievement).order_by(Achievement.id)).all());earned={x.achievement_id for x in s.scalars(select(ChildAchievement).where(ChildAchievement.child_id==child_id)).all()}
        return [(a,a.id in earned) for a in all_items]
def award(child_id,code):
    with SessionLocal() as s:
        a=s.scalar(select(Achievement).where(Achievement.code==code))
        if not a:return False
        exists=s.scalar(select(ChildAchievement).where(ChildAchievement.child_id==child_id,ChildAchievement.achievement_id==a.id))
        if exists:return False
        s.add(ChildAchievement(child_id=child_id,achievement_id=a.id));s.commit();return True
def auto_award(child_id):
    with SessionLocal() as s:
        lesson_count=s.scalar(select(func.count()).select_from(Progress).where(Progress.child_id==child_id)) or 0
        test_count=s.scalar(select(func.count()).select_from(TestResult).where(TestResult.child_id==child_id)) or 0
        word_count=s.scalar(select(func.count()).select_from(ReviewItem).where(ReviewItem.child_id==child_id)) or 0
        earned=[]
        if lesson_count>=1:earned.append("first_lesson")
        if word_count>=5:earned.append("five_words")
        if test_count>=1:earned.append("first_test")
    for code in earned:award(child_id,code)
