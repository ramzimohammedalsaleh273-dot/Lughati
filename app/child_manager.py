"""إدارة ملفات الأطفال بشكل آمن وموحد."""
from app.database import SessionLocal
from app.models import Child, Progress, ReviewItem, DailyPlan, TestResult, AssessmentAttempt, Recording, ChildAchievement
from sqlalchemy import select

def create_child(name, age=6):
    name=str(name).strip()
    age=int(age)
    if not name: raise ValueError("اسم الطفل مطلوب")
    if not 4 <= age <= 99: raise ValueError("العمر غير صالح")
    with SessionLocal() as s:
        child=Child(name=name, age=age); s.add(child); s.commit(); s.refresh(child)
        return child.id

def update_child(child_id, name=None, age=None):
    with SessionLocal() as s:
        c=s.get(Child,int(child_id))
        if not c: raise ValueError("الطفل غير موجود")
        if name is not None:
            name=str(name).strip()
            if not name: raise ValueError("اسم الطفل مطلوب")
            c.name=name
        if age is not None:
            age=int(age)
            if not 4 <= age <= 99: raise ValueError("العمر غير صالح")
            c.age=age
        s.commit(); return c.id

def delete_child(child_id):
    child_id=int(child_id)
    with SessionLocal() as s:
        c=s.get(Child,child_id)
        if not c: return False
        # العلاقات التي لا تملك cascade في النموذج الحالي تنظف يدوياً.
        for model in (Progress,ReviewItem,DailyPlan,TestResult,AssessmentAttempt,Recording,ChildAchievement):
            s.query(model).filter_by(child_id=child_id).delete(synchronize_session=False)
        s.delete(c); s.commit(); return True
