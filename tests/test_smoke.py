from app.database import init_db
from app.seed import seed_content
from app.services import lessons,words

def test_database_and_seed():
    init_db(); seed_content(); assert lessons("ar"); assert lessons("en"); assert words("ar"); assert words("en")
