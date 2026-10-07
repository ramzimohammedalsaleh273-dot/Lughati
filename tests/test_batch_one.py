from app.database import init_db,SessionLocal
from app.seed import seed_content
from app.models import Lesson,Activity,Question,Story,Word
from app.learning_engine import learning_snapshot,level_gate,ensure_review_items
from app.curriculum_engine import outcomes,AGE_GROUPS,SKILLS

def test_batch_one_content_and_skills():
    init_db(); seed_content()
    with SessionLocal() as s:
        for lang in ("ar","en"):
            assert s.query(Lesson).filter_by(language=lang).count() >= 78
            assert s.query(Word).filter_by(language=lang).count() >= 100
            assert s.query(Story).filter_by(language=lang).count() >= 13
            assert s.query(Question).filter_by(language=lang).count() >= 156
            assert s.query(Activity).join(Lesson).filter(Lesson.language==lang).count() >= 312
            assert {x.skill for x in s.query(Question).filter_by(language=lang).all()} >= set(SKILLS)

def test_batch_one_curriculum_and_mastery_engine():
    init_db(); seed_content()
    with SessionLocal() as s:
        child=s.query(__import__("app.models",fromlist=["Child"]).Child).first()
    assert len(AGE_GROUPS)==5
    for lang in ("ar","en"):
        for age in AGE_GROUPS:
            assert len(outcomes(lang,0,age))==6
        gate=level_gate(child.id,lang,0)
        assert gate.level==0 and not gate.ready
        snap=learning_snapshot(child.id,lang)
        assert snap["current_level"]==0
    assert ensure_review_items(child.id,"ar",0)>=1
