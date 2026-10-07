from app.database import init_db,SessionLocal
from app.seed import seed_content
from app.models import Lesson,Word,Story,Question,Activity,MediaAsset

def test_rich_first_half_content():
    init_db(); seed_content()
    with SessionLocal() as s:
        for lang in ("ar","en"):
            assert s.query(Lesson).filter_by(language=lang).count() >= 78
            assert s.query(Word).filter_by(language=lang).count() >= 100
            assert s.query(Story).filter_by(language=lang).count() >= 13
            assert s.query(Question).filter_by(language=lang).count() >= 78
            assert s.query(MediaAsset).filter_by(language=lang).count() >= 26
        assert s.query(Activity).count() >= 400

def test_all_core_skills_have_questions():
    init_db(); seed_content()
    skills={"listening","speaking","reading","writing","vocabulary","grammar"}
    with SessionLocal() as s:
        for lang in ("ar","en"):
            got={x.skill for x in s.query(Question).filter_by(language=lang).all()}
            assert skills <= got
