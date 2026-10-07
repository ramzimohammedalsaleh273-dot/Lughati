import json
from app.database import SessionLocal
from app.models import Child, Lesson, Word, Story, Question, Achievement, Activity, MediaAsset, ParentProfile, UserSetting
from app.first_half_content import build_rich_content

def _lesson(s, data):
    row=s.query(Lesson).filter_by(language=data["language"],level=data["level"],title=data["title"]).first()
    if not row:
        row=Lesson(language=data["language"],level=data["level"],title=data["title"],skill=data["skill"],body=data["body"])
        s.add(row); s.flush()
    return row

def _word(s, data):
    if not s.query(Word).filter_by(language=data["language"],text=data["text"]).first():
        s.add(Word(**data))

def _story(s, data):
    if not s.query(Story).filter_by(language=data["language"],level=data["level"],title=data["title"]).first():
        s.add(Story(language=data["language"],level=data["level"],title=data["title"],body=data["body"],questions="[]"))

def _question(s, data):
    if not s.query(Question).filter_by(language=data["language"],level=data["level"],prompt=data["prompt"]).first():
        options={"type":data["type"],"options":data["options"]}
        s.add(Question(language=data["language"],level=data["level"],skill=data["skill"],prompt=data["prompt"],options=json.dumps(options,ensure_ascii=False),answer=data["answer"]))

def seed_content():
    lessons,words,stories,questions=build_rich_content()
    with SessionLocal() as s:
        child=s.query(Child).first()
        if not child:
            child=Child(name="الطفل",age=6); s.add(child)
        if not s.query(ParentProfile).first():
            s.add(ParentProfile(name="ولي الأمر"))
        defaults={"language":"ar","offline_first":"true","theme":"فاتح","daily_minutes":"20","content_version":"1"}
        for key,value in defaults.items():
            if not s.query(UserSetting).filter_by(key=key).first():
                s.add(UserSetting(key=key,value=value))
        for data in lessons:
            row=_lesson(s,data)
            kinds=[
                ("تهيئة", "اقرأ هدف النشاط وافهم المطلوب قبل البدء."),
                ("تطبيق", "نفذ النشاط وحدك ثم قارن النتيجة بالنموذج."),
                ("مراجعة", "أعد النشاط مع مثال جديد حتى تثبت المهارة.")
            ]
            for order,(kind,instruction) in enumerate(kinds,1):
                exists=s.query(Activity).filter_by(lesson_id=row.id,order_no=order).first()
                if not exists:
                    s.add(Activity(lesson_id=row.id,kind=kind,instruction=instruction,content=data["body"],order_no=order))
        for data in words: _word(s,data)
        for data in stories: _story(s,data)
        for data in questions: _question(s,data)
        for lang in ("ar","en"):
            for level in range(13):
                for kind,title in (("audio","تدريب صوتي" if lang=="ar" else "Audio Practice"),("video","درس مرئي" if lang=="ar" else "Video Lesson")):
                    exists=s.query(MediaAsset).filter_by(language=lang,level=level,kind=kind).first()
                    if not exists:
                        s.add(MediaAsset(language=lang,level=level,kind=kind,title=title,path="",source="",offline_ready=False))
        achievements=[
            ("first_lesson","أول درس","أكمل أول درس."),
            ("five_words","خمس كلمات","راجع خمس مفردات."),
            ("first_test","أول اختبار","أكمل أول اختبار."),
            ("story_reader","قارئ القصص","اقرأ قصة."),
            ("ten_lessons","عشرة دروس","أكمل عشرة دروس."),
            ("master_level","إتقان مستوى","أتقن دروس مستوى كامل."),
            ("daily_streak","مواظب","أكمل خطة يومية."),
            ("skill_balanced","متوازن","حقق تقدماً في المهارات الست."),
        ]
        for code,title,description in achievements:
            if not s.query(Achievement).filter_by(code=code).first():
                s.add(Achievement(code=code,title=title,description=description))
        s.commit()
