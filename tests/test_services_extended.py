from app.database import init_db, SessionLocal
from app.seed import seed_content
from app.services import children, get_child, progress_for, create_daily_plan, complete_daily_plan, achievement_status
from app.models import Child

def test_child_and_daily_plan_flow():
    init_db(); seed_content()
    c=get_child()
    assert c is not None
    p=create_daily_plan(c.id,"ar",25)
    assert p.minutes==25
    assert complete_daily_plan(c.id,"ar")
    assert children()
    assert progress_for(c.id,"ar") == [] or isinstance(progress_for(c.id,"ar"),list)
    assert achievement_status(c.id)
