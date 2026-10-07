"""فحوصات اتساق المحتوى وقاعدة البيانات قبل التشغيل."""
from sqlalchemy import inspect,select
from app.database import engine,SessionLocal
from app.models import Child,Lesson,Word,Story,Question,Activity,Achievement

REQUIRED_TABLES=("children","lessons","words","progress","test_results","review_items","stories","questions","activities","achievements")

def validate_schema():
    tables=set(inspect(engine).get_table_names())
    missing=[x for x in REQUIRED_TABLES if x not in tables]
    return {"ok":not missing,"missing":missing}

def validate_content():
    with SessionLocal() as s:
        langs={}
        for lang in ("ar","en"):
            langs[lang]={
                "lessons":s.query(Lesson).filter_by(language=lang).count(),
                "words":s.query(Word).filter_by(language=lang).count(),
                "stories":s.query(Story).filter_by(language=lang).count(),
                "questions":s.query(Question).filter_by(language=lang).count(),
                "activities":s.query(Activity).join(Lesson,Activity.lesson_id==Lesson.id).filter(Lesson.language==lang).count(),
            }
        ach=s.query(Achievement).count()
    return {"languages":langs,"achievements":ach,"ok":all(v["lessons"]>=78 and v["words"]>=100 and v["stories"]>=13 and v["questions"]>=78 for v in langs.values())}

def full_check():
    a=validate_schema(); b=validate_content(); return {"schema":a,"content":b,"ok":a["ok"] and b["ok"]}
