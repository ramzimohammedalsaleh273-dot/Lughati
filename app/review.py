from datetime import datetime,timedelta
from sqlalchemy import select
from app.database import SessionLocal
from app.models import ReviewItem

def schedule(child_id,word_id,quality):
    quality=max(0,min(5,int(quality)))
    with SessionLocal() as s:
        item=s.scalar(select(ReviewItem).where(ReviewItem.child_id==child_id,ReviewItem.word_id==word_id))
        if not item: item=ReviewItem(child_id=child_id,word_id=word_id); s.add(item)
        if quality<3: item.repetitions=0; days=1; item.state="error"
        else:
            item.repetitions+=1; days=1 if item.repetitions==1 else 3 if item.repetitions==2 else 7 if item.repetitions==3 else 14; item.state="mastered" if item.repetitions>=5 else "review"
        item.next_review=datetime.utcnow()+timedelta(days=days); s.commit()

def due(child_id):
    with SessionLocal() as s: return list(s.scalars(select(ReviewItem).where(ReviewItem.child_id==child_id,ReviewItem.next_review<=datetime.utcnow()).order_by(ReviewItem.next_review)))
