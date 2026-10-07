from app.database import init_db,SessionLocal
from app.seed import seed_content
from app.models import Child
from app.game_engine import MODES,round_for,check
from app.learning_engine import ensure_review_items
from app.adaptive_learning import recommendations,plan_minutes
from app.media_engine import assets
from app.story_engine import build_session

def test_batch_two_engines():
    init_db();seed_content()
    with SessionLocal() as s:c=s.query(Child).first()
    ensure_review_items(c.id,"ar",0)
    from app.services import words,stories
    ws=words("ar")
    for mode in MODES:
        r=round_for(mode,ws)
        assert r and r.answer
        assert check(r,r.answer)
    assert recommendations(c.id,"ar")
    assert plan_minutes(c.id,"ar",20)
    assert len(assets("ar"))>=13
    assert build_session(stories("ar")[0]).body
