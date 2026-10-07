from app.database import init_db
from app.seed import seed_content
from app.assessment import load_questions, options, grade, finish

def test_assessment_engine():
    init_db(); seed_content()
    questions=load_questions("ar",0,limit=5)
    assert len(questions)>=3
    assert options(questions[0])
    assert grade(questions[0],questions[0].answer)
