"""حماية وظائف ولي الأمر والتحقق من المدخلات."""
from app.auth import verify_parent_pin, parent_pin_enabled, set_parent_pin

def require_parent(pin):
    if not parent_pin_enabled(): return True
    return bool(verify_parent_pin(pin))

def change_parent_pin(old_pin,new_pin):
    if parent_pin_enabled() and not verify_parent_pin(old_pin):
        raise PermissionError("رمز ولي الأمر الحالي غير صحيح")
    new_pin=str(new_pin).strip()
    if not new_pin.isdigit() or len(new_pin)<4: raise ValueError("رمز ولي الأمر يجب أن يكون أرقاماً من 4 خانات أو أكثر")
    return set_parent_pin(new_pin)
