"""مزامنة قابلة لإعادة المحاولة دون فقد الأحداث."""
from app.database import SessionLocal
from app.models import SyncEvent
from app.sync import push

def retry_failed(limit=100):
    with SessionLocal() as s:
        rows=s.query(SyncEvent).filter_by(status="failed").order_by(SyncEvent.id).limit(int(limit)).all()
        for row in rows: row.status="pending"
        s.commit()
    return len(rows)

def mark_failed(event_ids):
    with SessionLocal() as s:
        count=0
        for eid in event_ids:
            row=s.get(SyncEvent,int(eid))
            if row: row.status="failed"; count+=1
        s.commit()
    return count

def sync_now(endpoint, token=None, limit=50):
    if not str(endpoint).strip(): raise ValueError("رابط المزامنة مطلوب")
    return push(str(endpoint).strip(),token=token,limit=int(limit))

def queue_count():
    with SessionLocal() as s:
        return {status:s.query(SyncEvent).filter_by(status=status).count() for status in ("pending","synced","failed")}
