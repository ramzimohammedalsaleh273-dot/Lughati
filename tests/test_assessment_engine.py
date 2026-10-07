from app.database import init_db
from app.seed import seed_content
from app.assessment import load_questions, options, grade

def test_assessment_engine():
    init_db(); seed_content()
    questions=load_questions("ar",0,limit=12)
    assert len(questions)>=6
    choice_question=next(q for q in questions if options(q))
    assert options(choice_question)
    assert grade(choice_question,choice_question.answer)
