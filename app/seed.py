import json
from pathlib import Path
from app.database import SessionLocal
from app.models import Child, Lesson, Word, Story, Question, Achievement, Activity, MediaAsset, ParentProfile, UserSetting, CurriculumUnit
from app.content_authoring import build_content
from app.vocabulary_pack import AR_EXTRA, EN_EXTRA
from app.complete_content import build_age_units, build_extended_words, build_age_stories
from app.media_factory import ensure_media

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
        s.add(Story(language=data["language"],level=data["level"],title=data["title"],body=data["body"],questions=json.dumps(data.get("questions",[]),ensure_ascii=False)))

def _question(s, data):
    if not s.query(Question).filter_by(language=data["language"],level=data["level"],prompt=data["prompt"]).first():
        options={"type":data["type"],"options":data["options"]}
        s.add(Question(language=data["language"],level=data["level"],skill=data["skill"],prompt=data["prompt"],options=json.dumps(options,ensure_ascii=False),answer=data["answer"]))

def _unit(s, data, kind="lesson", payload=None):
    row=s.query(CurriculumUnit).filter_by(language=data["language"],age_group=data["age_group"],level=data["level"],skill=data.get("skill",""),kind=kind,title=data["title"]).first()
    if not row:
        s.add(CurriculumUnit(language=data["language"],age_group=data["age_group"],level=data["level"],skill=data.get("skill",""),kind=kind,title=data["title"],body=data["body"],payload=json.dumps(payload or {},ensure_ascii=False)))

def seed_content():
    lessons,words,stories,questions=build_content()
    age_units=build_age_units()
    extended_words=build_extended_words()
    age_stories=build_age_stories()
    with SessionLocal() as s:
        child=s.query(Child).first()
        if not child: child=Child(name="الطفل",age=6); s.add(child)
        if not s.query(ParentProfile).first(): s.add(ParentProfile(name="ولي الأمر"))
        defaults={"language":"ar","offline_first":"true","theme":"فاتح","daily_minutes":"20","content_version":"2","age_curriculum":"5"}
        for key,value in defaults.items():
            if not s.query(UserSetting).filter_by(key=key).first(): s.add(UserSetting(key=key,value=value))
        for data in lessons:
            row=_lesson(s,data)
            kinds=[(a["kind"],a["instruction"]) for a in data.get("activities",[])] or [("تهيئة","راجع المعرفة السابقة."),("تطبيق","نفذ النشاط."),("مراجعة","أعد النشاط.")]
            for order,(kind,instruction) in enumerate(kinds,1):
                if not s.query(Activity).filter_by(lesson_id=row.id,order_no=order).first():
                    s.add(Activity(lesson_id=row.id,kind=kind,instruction=instruction,content=data["body"],order_no=order))
        for data in words: _word(s,data)
        for data in extended_words: _word(s,data)
        for lang,extra in (("ar",AR_EXTRA),("en",EN_EXTRA)):
            for level in range(13):
                for idx,(term,meaning,example) in enumerate(extra):
                    if idx % 2 == level % 2: _word(s,{"language":lang,"text":term,"meaning":meaning,"example":example,"level":level})
        for data in stories: _story(s,data)
        for data in questions: _question(s,data)
        for u in age_units: _unit(s,u,"lesson")
        for st in age_stories: _unit(s,st,"story",{"questions":st["questions"]})
        media_root=ensure_media(Path(__file__).resolve().parents[1]/"media")
        for item in ("ar","en"):
            for level in range(13):
                for kind,title,sub in (("image","صورة تعليمية" if item=="ar" else "Learning Image","images"),("audio","تدريب صوتي" if item=="ar" else "Audio Practice","audio"),("video","درس مرئي" if item=="ar" else "Video Lesson","video")):
                    ext={"image":"svg","audio":"wav","video":"mp4"}[kind]
                    path=str(Path(media_root[sub])/f"{item}_{level:02d}.{ext}")
                    exists=s.query(MediaAsset).filter_by(language=item,level=level,kind=kind).first()
                    if not exists: s.add(MediaAsset(language=item,level=level,kind=kind,title=title,path=path,source="generated_local_offline",offline_ready=Path(path).exists()))
                    else: exists.path=path; exists.offline_ready=Path(path).exists()
        for code,title,description in [
            ("first_lesson","أول درس","أكمل أول درس."),("five_words","خمس كلمات","راجع خمس مفردات."),("five_lessons","خمسة دروس","أكمل خمسة دروس."),("first_test","أول اختبار","أكمل أول اختبار."),("story_reader","قارئ القصص","اقرأ قصة."),("ten_lessons","عشرة دروس","أكمل عشرة دروس."),("master_level","إتقان مستوى","أتقن دروس مستوى كامل."),("daily_streak","مواظب","أكمل خطة يومية."),("skill_balanced","متوازن","حقق تقدماً في المهارات الست."),("adventure_starter","بداية المغامرة","أكمل أول مهمة في عالم المغامرة."),("media_ready","مستعد للوسائط","شغّل مادة صوتية ومرئية وصورة محلية.")
        ]:
            if not s.query(Achievement).filter_by(code=code).first(): s.add(Achievement(code=code,title=title,description=description))
        s.commit()
    from app.settings_service import ensure_defaults
    ensure_defaults()
