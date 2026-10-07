import hashlib, os, hmac
from app.database import SessionLocal
from app.models import ParentProfile

def _hash(pin, salt):
    return hashlib.pbkdf2_hmac("sha256",pin.encode(),salt,120000).hex()

def set_parent_pin(pin):
    pin=str(pin).strip()
    if not pin.isdigit() or len(pin)<4: raise ValueError("الرمز يجب أن يكون أرقاماً من 4 خانات على الأقل")
    salt=os.urandom(16)
    with SessionLocal() as s:
        p=s.query(ParentProfile).first()
        if not p: p=ParentProfile(name="ولي الأمر"); s.add(p)
        p.pin_hash=salt.hex()+":"+_hash(pin,salt); s.commit()
    return True

def verify_parent_pin(pin):
    with SessionLocal() as s:
        p=s.query(ParentProfile).first()
        if not p or not p.pin_hash or ":" not in p.pin_hash:return False
        try:
            raw,digest=p.pin_hash.split(":",1); salt=bytes.fromhex(raw)
            return hmac.compare_digest(_hash(str(pin).strip(),salt),digest)
        except (ValueError,TypeError): return False

def parent_pin_enabled():
    with SessionLocal() as s:
        p=s.query(ParentProfile).first()
        return bool(p and p.pin_hash)
