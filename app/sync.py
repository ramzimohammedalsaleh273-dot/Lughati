import json
from datetime import datetime
from urllib.request import Request,urlopen
from app.database import SessionLocal
from app.models import SyncEvent

def queue(entity,entity_id,operation,payload):
    with SessionLocal() as s:
        row=SyncEvent(entity=entity,entity_id=int(entity_id),operation=operation,payload=json.dumps(payload,ensure_ascii=False),status="pending")
        s.add(row); s.commit(); return row.id

def pending(limit=100):
    with SessionLocal() as s:
        return list(s.query(SyncEvent).filter_by(status="pending").order_by(SyncEvent.id).limit(limit).all())

def push(endpoint,token=None,limit=50):
    events=pending(limit)
    if not events:return {"sent":0,"failed":0}
    body={"events":[{"id":e.id,"entity":e.entity,"entity_id":e.entity_id,"operation":e.operation,"payload":json.loads(e.payload)} for e in events]}
    data=json.dumps(body,ensure_ascii=False).encode()
    headers={"Content-Type":"application/json"}
    if token:headers["Authorization"]="Bearer "+str(token)
    request=Request(endpoint,data=data,headers=headers,method="POST")
    try:
        with urlopen(request,timeout=20) as response:
            if not 200<=response.status<300: raise RuntimeError(f"HTTP {response.status}")
        with SessionLocal() as s:
            for e in events:
                row=s.get(SyncEvent,e.id)
                if row:row.status="synced";row.synced_at=datetime.utcnow()
            s.commit()
        return {"sent":len(events),"failed":0}
    except Exception as exc:
        return {"sent":0,"failed":len(events),"error":str(exc)}

def status():
    with SessionLocal() as s:
        return {"pending":s.query(SyncEvent).filter_by(status="pending").count(),"synced":s.query(SyncEvent).filter_by(status="synced").count()}
