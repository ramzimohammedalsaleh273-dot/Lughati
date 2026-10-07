from app.database import init_db
from app.seed import seed_content
from app.services import lessons,stories,questions,words
from app.placement import recommended_level,age_group

def test_curriculum_and_content():
    init_db(); seed_content()
    assert len(lessons('ar'))>=13
    assert len(lessons('en'))>=13
    assert stories('ar'); assert stories('en')
    assert questions('ar'); assert questions('en')
    assert len(words('ar'))>=20 and len(words('en'))>=20

def test_placement():
    assert recommended_level(35)==0
    assert recommended_level(75)==8
    assert recommended_level(95)==12
    assert age_group(5)=='4–5'; assert age_group(17)=='14+'
