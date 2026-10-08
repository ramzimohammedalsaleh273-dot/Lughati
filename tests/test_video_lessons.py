from app.video_lesson_engine import build_video_script
def test_video_script_has_characters_scenes_and_interactions():
    s=build_video_script("ar","6–7",1,"الحروف","قراءة","تعلم الحرف")
    assert s["characters"]==["ليان","سامي"]
    assert len(s["scenes"])>=7
    assert any(x.get("interaction") for x in s["scenes"])
    assert s["requirements"]["human_voice"] is True
