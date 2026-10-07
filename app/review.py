from datetime import datetime,timedelta
from sqlalchemy import select
from app.database import SessionLocal
from app.models import ReviewItem,Word

def schedule(child_id,word_id,quality):
    quality=max(0,min(5,int(quality)))
    with SessionLocal() as s:
        item=s.scalar(select(ReviewItem).where(ReviewItem.child_id==child_id,ReviewItem.word_id==word_id))
        if not item:
            item=ReviewItem(child_id=child_id,word_id=word_id,state="new",ease=2.5,repetitions=0)
            s.add(item)
        if quality<3:
            item.repetitions=0
            item.ease=max(1.3,float(item.ease)-0.2)
            days=1
            item.state="error"
        else:
            item.repetitions+=1
            item.ease=max(1.3,float(item.ease)+(0.1-(5-quality)*0.08))
            if item.repetitions==1: days=1
            elif item.repetitions==2: days=3
            elif item.repetitions==3: days=7
            else: days=max(14,round(14*(float(item.ease)**max(0,item.repetitions-3))))
            item.state="mastered" if item.repetitions>=5 and quality>=4 else "review"
        item.next_review=datetime.utcnow()+timedelta(days=days)
        s.commit()
        return {"repetitions":item.repetitions,"ease":round(item.ease,2),"days":days,"state":item.state}

def due(child_id,limit=50):
    with SessionLocal() as s:
        return list(s.execute(
            select(ReviewItem,Word).join(Word,Word.id==ReviewItem.word_id)
            .where(ReviewItem.child_id==child_id,ReviewItem.next_review<=datetime.utcnow())
            .order_by(ReviewItem.next_review)
            .limit(max(1,int(limit)))
        ).all())

def upcoming(child_id,limit=50):
    with SessionLocal() as s:
        return list(s.scalars(
            select(ReviewItem).where(ReviewItem.child_id==child_id)
            .order_by(ReviewItem.next_review).limit(max(1,int(limit)))
        ))
