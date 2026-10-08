import json
from app.database import SessionLocal
from app.models import VideoLesson,VideoInteraction
from app.video_lesson_engine import build_video_script
def ensure_video_lessons(units):
    created=0
    with SessionLocal() as s:
        for u in units:
            exists=s.query(VideoLesson).filter_by(curriculum_unit_id=u.id).first()
            if exists: continue
            script=build_video_script(u.language,u.age_group,u.level,u.title,u.skill,u.body)
            row=VideoLesson(language=u.language,age_group=u.age_group,level=u.level,curriculum_unit_id=u.id,title=u.title,character=script["characters"][0],status="script_ready",manifest=json.dumps(script,ensure_ascii=False))
            s.add(row); s.flush()
            for scene in script["scenes"]:
                inter=scene.get("interaction")
                if inter:
                    s.add(VideoInteraction(video_lesson_id=row.id,order_no=scene["order"],kind=inter["kind"],prompt=inter["prompt"],payload=json.dumps(inter,ensure_ascii=False)))
            created+=1
        s.commit()
    return created
def video_lessons(language=None,age_group=None,level=None):
    with SessionLocal() as s:
        q=s.query(VideoLesson)
        if language:q=q.filter_by(language=language)
        if age_group:q=q.filter_by(age_group=age_group)
        if level is not None:q=q.filter_by(level=level)
        return q.order_by(VideoLesson.level,VideoLesson.id).all()
