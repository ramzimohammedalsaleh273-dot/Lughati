from app.database import init_db,SessionLocal
from app.seed import seed_content
from app.validation import full_check
from app.curriculum_engine import curriculum_matrix
from app.progress_engine import snapshot

def test_curriculum_matrix():
    for lang in ("ar","en"):
        matrix=curriculum_matrix(lang)
        assert len(matrix)==13
        assert all(len(v)==6 for v in matrix.values())

def test_validation_and_snapshot():
    init_db(); seed_content()
    result=full_check()
    assert result["ok"], result
    with SessionLocal() as s:
        child=s.query(__import__("app.models",fromlist=["Child"]).Child).first()
    snap=snapshot(child.id,"ar")
    assert snap["lessons"]>=78
