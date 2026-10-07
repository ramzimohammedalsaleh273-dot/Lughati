import hashlib, os
from app.database import SessionLocal
from app.models import ParentProfile

def _hash(pin, salt):
    return hashlib.pbkdf2_hmac("sha256",pin.encode(),salt,120000).hex()

def set_parent_pin(pin):
    pin=str(pin).strip()
    if len(pin)<4: raise ValueError("الرمز يجب أن يكون 4 أرقام على الأقل")
    salt=os.urandom(16)
    with SessionLocal() as s:
        p=s.query(ParentProfile).first()
        if not p:
            p=ParentProfile(name="ولي الأمر"); s.add(p)
        p.pin_hash=salt.hex()+":"+_hash(pin,salt); s.commit()
    return True

def verify_parent_pin(pin):
    with SessionLocal() as s:
        p=s.query(ParentProfile).first()
        if not p or not p.pin_hash or ":" not in p.pin_hash:return False
        raw,digest=p.pin_hash.split(":",1)
        salt=bytes.fromhex(raw)
        return _hash(str(pin).strip(),salt)==digest

def parent_pin_enabled():
    with SessionLocal() as s:
        p=s.query(ParentProfile).first()
        return bool(p and p.pin_hash)
