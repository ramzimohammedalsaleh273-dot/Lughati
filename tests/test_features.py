from app.database import init_db,SessionLocal
from app.seed import seed_content
from app.models import Child

def test_learning_core():
    init_db(); seed_content(); c=SessionLocal().query(Child).first(); assert c and c.name
