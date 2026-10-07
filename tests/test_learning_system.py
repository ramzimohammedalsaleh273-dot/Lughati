from app.database import init_db
from app.seed import seed_content
from app.services import lessons,stories,questions,words
from app.placement import recommended_level,age_group

def test_curriculum_and_content():
    init_db(); seed_content()
    assert len(lessons('ar'))>=39
    assert len(lessons('en'))>=39
    assert len(stories('ar'))>=13; assert len(stories('en'))>=13
    assert len(questions('ar'))>=39; assert len(questions('en'))>=39
    assert len(words('ar'))>=50 and len(words('en'))>=50

def test_placement():
    assert recommended_level(35)==0
    assert recommended_level(75)==8
    assert recommended_level(95)==12
    assert age_group(5)=='4–5'; assert age_group(17)=='14+'
