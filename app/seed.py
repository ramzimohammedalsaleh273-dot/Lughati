import json
from app.database import SessionLocal
from app.models import Child, Lesson, Word, Story, Question, Achievement
from app.curriculum import ARABIC_LEVELS, ENGLISH_LEVELS
from app.content_pack import ARABIC_BODIES, ENGLISH_BODIES

AR_WORD_BANK=[
("أب","father"),("أم","mother"),("بيت","house"),("باب","door"),("كتاب","book"),("قلم","pen"),
("مدرسة","school"),("معلم","teacher"),("طالب","student"),("ماء","water"),("طعام","food"),("شمس","sun"),
("قمر","moon"),("سماء","sky"),("أرض","earth"),("شجرة","tree"),("زهرة","flower"),("بحر","sea"),
("سيارة","car"),("طريق","road"),("صديق","friend"),("أسرة","family"),("ولد","boy"),("بنت","girl"),
("يقرأ","reads"),("يكتب","writes"),("يذهب","goes"),("يأتي","comes"),("يجلس","sits"),("يقوم","stands"),
("كبير","big"),("صغير","small"),("جميل","beautiful"),("جديد","new"),("قديم","old"),("سريع","fast"),
("بطيء","slow"),("اليوم","today"),("غداً","tomorrow"),("أمس","yesterday"),("واحد","one"),("اثنان","two"),
("ثلاثة","three"),("أربعة","four"),("خمسة","five"),("أين","where"),("متى","when"),("كيف","how"),
("لماذا","why"),("نعم","yes"),("لا","no"),("صباح","morning"),("مساء","evening"),("لغة","language"),
("تعلم","learning"),("قراءة","reading"),("كتابة","writing"),("استماع","listening"),("تحدث","speaking")
]
EN_WORD_BANK=[
("father","أب"),("mother","أم"),("house","بيت"),("door","باب"),("book","كتاب"),("pen","قلم"),
("school","مدرسة"),("teacher","معلم"),("student","طالب"),("water","ماء"),("food","طعام"),("sun","شمس"),
("moon","قمر"),("sky","سماء"),("earth","أرض"),("tree","شجرة"),("flower","زهرة"),("sea","بحر"),
("car","سيارة"),("road","طريق"),("friend","صديق"),("family","أسرة"),("boy","ولد"),("girl","بنت"),
("read","يقرأ"),("write","يكتب"),("go","يذهب"),("come","يأتي"),("sit","يجلس"),("stand","يقوم"),
("big","كبير"),("small","صغير"),("beautiful","جميل"),("new","جديد"),("old","قديم"),("fast","سريع"),
("slow","بطيء"),("today","اليوم"),("tomorrow","غداً"),("yesterday","أمس"),("one","واحد"),("two","اثنان"),
("three","ثلاثة"),("four","أربعة"),("five","خمسة"),("where","أين"),("when","متى"),("how","كيف"),
("why","لماذا"),("yes","نعم"),("no","لا"),("morning","صباح"),("evening","مساء"),("language","لغة"),
("learning","تعلم"),("reading","قراءة"),("writing","كتابة"),("listening","استماع"),("speaking","تحدث")
]

AR_STORY_TEMPLATES=[
("بداية الحروف","بدأ الطفل يتعرف إلى الأصوات والحروف من حوله."),
("أصدقاء الحروف","تعرّف الطفل إلى أشكال الحروف وربطها بأصواتها."),
("رحلة الحركات","تدرب الطفل على الفتحة والضمة والكسرة والمدود."),
("كلمات من حياتنا","قرأ الطفل كلمات قصيرة واستعملها في مواقف يومية."),
("جمل مفيدة","بنى الطفل جملاً اسمية ووصف الأشياء من حوله."),
("أفعال يومية","استخدم الطفل الأفعال والفاعل في جمل صحيحة."),
("قارئ صغير","قرأ الطفل نصاً قصيراً وحدد فكرته وتفاصيله."),
("يوم الكتابة","كتب الطفل كلمات وجملاً وأتقن بعض قواعد الإملاء."),
("مغامرة القواعد","استخدم الطفل الضمائر والمذكر والمؤنث وحروف الجر."),
("حديث جميل","تحدث الطفل عن يومه ووصف مكاناً يحبه."),
("ورشة النحو","حل الطفل تدريبات على التراكيب والنحو في سياقات حقيقية."),
("قارئ متأمل","قرأ الطفل نصاً أطول واستنتج المعاني ولخص الأفكار."),
("طلاقة اللغة","استخدم الطفل العربية في القراءة والكتابة والاستماع والتحدث.")
]
EN_STORY_TEMPLATES=[
("First Sounds","A learner starts by hearing and naming simple sounds."),
("Letter Friends","A learner connects letters with their common sounds."),
("Sound Blending","A learner blends short sounds and reads simple words."),
("Everyday Words","A learner uses useful words in familiar daily situations."),
("Simple Sentences","A learner builds clear short sentences and questions."),
("Daily Actions","A learner uses verbs and basic grammar in context."),
("A Young Reader","A learner reads a short text and finds its main idea."),
("Writing Day","A learner writes words, sentences and a short paragraph."),
("Grammar Adventure","A learner uses pronouns, prepositions and everyday phrases."),
("Useful Conversation","A learner talks about routines, places and preferences."),
("Grammar Workshop","A learner practises intermediate structures in context."),
("Thoughtful Reader","A learner reads longer text and infers meaning."),
("Functional English","A learner uses English for practical real-life tasks.")
]

def _add_lesson(s,lang,level,title,skill,body):
    if not s.query(Lesson).filter_by(language=lang,level=level,title=title).first():
        s.add(Lesson(language=lang,level=level,title=title,skill=skill,body=body))

def _add_word(s,lang,text,meaning,level,example):
    if not s.query(Word).filter_by(language=lang,text=text).first():
        s.add(Word(language=lang,text=text,meaning=meaning,level=level,example=example))

def _add_question(s,lang,level,skill,prompt,options,answer):
    if not s.query(Question).filter_by(language=lang,level=level,prompt=prompt).first():
        s.add(Question(language=lang,level=level,skill=skill,prompt=prompt,options=json.dumps(options,ensure_ascii=False),answer=answer))

def seed_content():
    with SessionLocal() as s:
        child=s.query(Child).first()
        if not child:
            s.add(Child(name="الطفل",age=6)); s.flush()

        for level in range(13):
            ar_title=ARABIC_LEVELS[level]; en_title=ENGLISH_LEVELS[level]
            _add_lesson(s,"ar",level,ar_title,"reading",ARABIC_BODIES[level])
            _add_lesson(s,"en",level,en_title,"reading",ENGLISH_BODIES[level])
            _add_lesson(s,"ar",level,f"{ar_title} — تدريب","practice",f"تدريب عملي للمستوى {level}: استماع وقراءة وكتابة وتطبيق.")
            _add_lesson(s,"en",level,f"{en_title} — Practice","practice",f"Practice for level {level}: listening, reading, writing and real use.")
            _add_lesson(s,"ar",level,f"{ar_title} — مراجعة","review",f"مراجعة تراكمية للمفردات والمهارات الأساسية في المستوى {level}.")
            _add_lesson(s,"en",level,f"{en_title} — Review","review",f"Cumulative review of vocabulary and core skills for level {level}.")
            if level < len(AR_STORY_TEMPLATES):
                st,body=AR_STORY_TEMPLATES[level]
                if not s.query(Story).filter_by(language="ar",level=level,title=st).first():
                    s.add(Story(language="ar",level=level,title=st,body=body,questions=json.dumps([{"prompt":"ما الفكرة الأساسية؟","answer":"التعلم والتطبيق"}],ensure_ascii=False)))
                st,body=EN_STORY_TEMPLATES[level]
                if not s.query(Story).filter_by(language="en",level=level,title=st).first():
                    s.add(Story(language="en",level=level,title=st,body=body,questions=json.dumps([{"prompt":"What is the main idea?","answer":"Learning and practice"}],ensure_ascii=False)))

            _add_question(s,"ar",level,"reading",f"المستوى {level}: اختر العبارة الصحيحة.",["التعلم والتطبيق","التوقف عن التعلم","حذف الكلمات"],"التعلم والتطبيق")
            _add_question(s,"ar",level,"vocabulary",f"المستوى {level}: ما معنى كلمة «كتاب»؟",["book","water","sun"],"book")
            _add_question(s,"ar",level,"writing",f"المستوى {level}: أي جملة مكتوبة بصورة صحيحة؟",["هذا كتاب.","هذا كتاب","كتاب هذا."],"هذا كتاب.")
            _add_question(s,"en",level,"reading",f"Level {level}: choose the best goal.",["Learning and practice","Stop learning","Delete words"],"Learning and practice")
            _add_question(s,"en",level,"vocabulary",f"Level {level}: What does “book” mean?",["كتاب","ماء","شمس"],"كتاب")
            _add_question(s,"en",level,"grammar",f"Level {level}: Choose the correct sentence.",["I have a book.","I has a book.","I having book."],"I have a book.")

        for i,(text,meaning) in enumerate(AR_WORD_BANK):
            _add_word(s,"ar",text,meaning,min(i//5,12),f"{text} في جملة مفيدة.")
        for i,(text,meaning) in enumerate(EN_WORD_BANK):
            _add_word(s,"en",text,meaning,min(i//5,12),f"Use “{text}” in a simple sentence.")

        achievements=[
            ("first_lesson","أول درس","أكمل أول درس."),
            ("five_words","خمس كلمات","تعلم خمس كلمات."),
            ("first_test","أول اختبار","أكمل أول اختبار."),
            ("story_reader","قارئ القصص","افتح قصة."),
            ("ten_lessons","عشرة دروس","أكمل عشرة دروس."),
            ("master_level","إتقان مستوى","أتقن دروس مستوى كامل."),
            ("daily_streak","مواظب","أكمل خطة يومية.")
        ]
        for code,title,desc in achievements:
            if not s.query(Achievement).filter_by(code=code).first():
                s.add(Achievement(code=code,title=title,description=desc))
        s.commit()
