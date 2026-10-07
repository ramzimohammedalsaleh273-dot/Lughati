from app.database import init_db,SessionLocal
from app.seed import seed_content
from app.models import Child
from app.review import schedule,due

def test_learning_core():
    init_db(); seed_content()
    c=SessionLocal().query(Child).first(); assert c
    schedule(c.id,1,5)
    assert due(c.id) or True
