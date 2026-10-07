from pathlib import Path
from app.complete_content import build_age_units,build_extended_words,build_age_stories
from app.media_factory import ensure_media
def test_age_curriculum_is_independent():
    rows=build_age_units()
    assert len(rows)==2*5*13*6
    assert len({(x["language"],x["age_group"],x["level"],x["skill"]) for x in rows})==780
def test_story_library_is_age_specific():
    rows=build_age_stories()
    assert len(rows)==2*5*13
def test_extended_vocabulary_has_real_items():
    rows=build_extended_words()
    assert len(rows)>=2*13*100
    assert all(x["text"] and x["example"] for x in rows)
def test_local_media_factory(tmp_path):
    root=ensure_media(tmp_path/"media")
    assert len(list((Path(root["images"])).glob("*.svg")))==26
    assert len(list((Path(root["audio"])).glob("*.wav")))==26
    # MP4 is created when ffmpeg exists; otherwise the app remains functional offline.
