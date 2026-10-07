from app.database import init_db
from app.seed import seed_content
from app.validation import full_check
from app.assessment import load_questions,grade
from app.models import Child

def test_full_learning_contract():
    init_db(); seed_content(); assert full_check()["ok"]
    from app.database import SessionLocal
    with SessionLocal() as s:c=s.query(Child).first()
    for lang in ("ar","en"):
        qs=load_questions(lang,0,limit=6); assert len(qs)>=6
        assert any(grade(q,q.answer) for q in qs)
