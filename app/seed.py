import json
from app.database import SessionLocal
from app.models import Child, Lesson, Word, Story, Question, Achievement, DailyPlan
from app.curriculum import ARABIC_LEVELS, ENGLISH_LEVELS
from app.content import AR_WORDS, EN_WORDS
from app.content_pack import ARABIC_BODIES, ENGLISH_BODIES

def seed_content():
    with SessionLocal() as s:
        if not s.query(Child).first():
            s.add(Child(name="الطفل", age=6)); s.flush()
        if s.query(Lesson).count() < 26:
            for level in range(13):
                at=ARABIC_LEVELS[level]
                et=ENGLISH_LEVELS[level]
                for title,skill,body in [
                    (at,"reading",f"الوحدة العربية {level}: {at}"),
                    (et,"reading",f"English level {level}: {et}"),
                ]:
                    lang="ar" if title==at else "en"
                    if not s.query(Lesson).filter_by(language=lang,level=level,title=title).first():
                        s.add(Lesson(language=lang,level=level,title=title,skill=skill,body=(ARABIC_BODIES[level] if lang=="ar" else ENGLISH_BODIES[level])))
        if s.query(Word).count() < len(AR_WORDS)+len(EN_WORDS):
            for level,(text,meaning) in enumerate(AR_WORDS):
                if not s.query(Word).filter_by(language="ar",text=text).first():
                    s.add(Word(language="ar",text=text,meaning=meaning,example=f"{text} مثال",level=min(level,12)))
            for level,(text,meaning) in enumerate(EN_WORDS):
                if not s.query(Word).filter_by(language="en",text=text).first():
                    s.add(Word(language="en",text=text,meaning=meaning,example=f"Example: {text}",level=min(level,12)))
        stories=[
          ("ar",0,"حكاية الحرف","كان حرف الألف يبحث عن أصدقائه. قابل باء وتاء، وتعلموا أن القراءة تبدأ من معرفة الحروف."),
          ("ar",4,"يوم في المدرسة","ذهب سامي إلى المدرسة، رتب كتبه وقرأ قصة قصيرة ثم كتب جملة جميلة."),
          ("ar",8,"رحلة إلى المكتبة","دخلت ليان المكتبة واختارت كتاباً مناسباً ثم جلست تقرأ بهدوء."),
          ("ar",12,"مغامرة اللغة","تعلم خالد كيف يستخدم القراءة والكتابة والاستماع والتحدث في يومه."),
          ("en",0,"A Little Cat","A little cat sees the sun. The cat runs and plays."),
          ("en",4,"At School","Maya goes to school. She reads a book and writes a sentence."),
          ("en",8,"At the Library","Maya visits the library, chooses a book and reads quietly."),
          ("en",12,"Language Adventure","Sam uses reading, writing, listening and speaking in everyday life.")
        ]
        for lang,level,title,body in stories:
            if not s.query(Story).filter_by(language=lang,title=title).first():
                s.add(Story(language=lang,level=level,title=title,body=body,questions=json.dumps([],ensure_ascii=False)))
        qs=[
          ("ar",0,"reading","ما أول حرف في كلمة «أب»؟",json.dumps(["أ","ب","ت"],ensure_ascii=False),"أ"),
          ("ar",2,"grammar","اختر الحركة في «بُ»",json.dumps(["الفتحة","الضمة","الكسرة"],ensure_ascii=False),"الضمة"),
          ("ar",4,"reading","أي جملة صحيحة؟",json.dumps(["هذا كتاب.","هذا كتب.","هذا كتابان."],ensure_ascii=False),"هذا كتاب."),
          ("en",0,"vocabulary","What is «cat»?",json.dumps(["قطة","كلب","كتاب"],ensure_ascii=False),"قطة"),
          ("en",2,"reading","Which word is CVC?",json.dumps(["cat","school","beautiful"],ensure_ascii=False),"cat"),
          ("en",4,"grammar","Choose: I ___ a book.",json.dumps(["have","has","having"],ensure_ascii=False),"have")
        ]
        for level in range(13):
            generated=[
              ("ar",level,"reading",f"ما هدف المستوى {level}؟",json.dumps(["التعلم والتطبيق","التوقف عن التعلم","حذف الكلمات"],ensure_ascii=False),"التعلم والتطبيق"),
              ("en",level,"reading",f"What is the goal of level {level}?",json.dumps(["Learning and practice","Stop learning","Delete words"],ensure_ascii=False),"Learning and practice")]
            for lang,lv,skill,prompt,options,answer in generated:
                if not s.query(Question).filter_by(language=lang,prompt=prompt).first():
                    s.add(Question(language=lang,level=lv,skill=skill,prompt=prompt,options=options,answer=answer))
        for lang,level,skill,prompt,options,answer in qs:
            if not s.query(Question).filter_by(language=lang,prompt=prompt).first():
                s.add(Question(language=lang,level=level,skill=skill,prompt=prompt,options=options,answer=answer))
        ach=[("first_lesson","أول درس","أكمل أول درس"),("five_words","خمس كلمات","تعلم خمس كلمات"),("first_test","أول اختبار","أكمل أول اختبار"),("story_reader","قارئ القصص","اقرأ قصة")]
        for code,title,desc in ach:
            if not s.query(Achievement).filter_by(code=code).first(): s.add(Achievement(code=code,title=title,description=desc))
        s.commit()
