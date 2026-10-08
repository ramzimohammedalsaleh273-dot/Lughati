from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from app.database import SessionLocal
from app.models import Child, Lesson, Progress, Word, Story, Achievement, DailyPlan, MediaAsset

LEVEL_TITLES = {
    "ar": ["التهيئة والأصوات", "الحروف وأشكالها", "الحركات والمقاطع", "الكلمات الأساسية",
           "الجملة الاسمية", "الجملة الفعلية", "القراءة والفهم", "الإملاء والكتابة",
           "النحو الأساسي", "التعبير والمحادثة", "النحو المتوسط", "القراءة المتقدمة", "الإتقان والتطبيق"],
    "en": ["Getting Ready", "Alphabet", "Phonics and Blending", "Core Vocabulary",
           "Simple Sentences", "Grammar Basics", "Reading", "Writing",
           "Grammar in Context", "Speaking", "Intermediate Grammar", "Advanced Reading", "Functional Mastery"],
}

SKILL_TITLES = {
    "listening": "الاستماع", "speaking": "التحدث", "reading": "القراءة",
    "writing": "الكتابة", "vocabulary": "المفردات", "grammar": "القواعد",
    "استماع": "الاستماع", "تحدث": "التحدث", "قراءة": "القراءة",
    "كتابة": "الكتابة", "مفردات": "المفردات", "تقويم": "التقويم",
}

class AppBackend(QObject):
    changed = Signal()

    def __init__(self):
        super().__init__()
        self._child_id = None
        self.refresh()

    def refresh(self):
        with SessionLocal() as s:
            child = s.query(Child).order_by(Child.id).first()
            if child:
                self._child_id = child.id
                self._child_name = child.name
                self._age = child.age
            else:
                self._child_id = None
                self._child_name = "الطفل"
                self._age = 6
            self._load_summary(s)
        self.changed.emit()

    def _load_summary(self, s):
        if not self._child_id:
            self._xp = 0
            self._streak = 0
            self._mastered = 0
            self._completed = 0
            return
        rows = s.query(Progress).filter_by(child_id=self._child_id).all()
        self._completed = len(rows)
        self._mastered = sum(1 for r in rows if r.mastered)
        self._xp = int(sum(max(0, r.score) for r in rows) * 10)
        self._streak = 1 if rows else 0

    @Property(str, notify=changed)
    def childName(self):
        return self._child_name

    @Property(int, notify=changed)
    def childAge(self):
        return self._age

    @Property(int, notify=changed)
    def xp(self):
        return self._xp

    @Property(int, notify=changed)
    def completedLessons(self):
        return self._completed

    @Property(int, notify=changed)
    def masteredLessons(self):
        return self._mastered

    @Property(int, notify=changed)
    def streak(self):
        return self._streak

    @Slot(str, result="QVariantList")
    def levels(self, language):
        language = language if language in LEVEL_TITLES else "ar"
        result = []
        with SessionLocal() as s:
            for level, title in enumerate(LEVEL_TITLES[language]):
                count = s.query(Lesson).filter_by(language=language, level=level).count()
                result.append({"level": level, "title": title, "lessonCount": count})
        return result

    @Slot(int, str, result="QVariantList")
    def lessons(self, level, language):
        result = []
        with SessionLocal() as s:
            rows = (s.query(Lesson).filter_by(level=level, language=language)
                    .order_by(Lesson.id).all())
            for stage, row in enumerate(rows, 1):
                result.append({
                    "id": row.id,
                    "language": row.language,
                    "level": row.level,
                    "stage": stage,
                    "title": row.title,
                    "stageTitle": SKILL_TITLES.get(row.skill, row.skill),
                    "skill": row.skill,
                    "body": row.body,
                    "done": self._lesson_done(s, row.id),
                })
        return result

    def _lesson_done(self, s, lesson_id):
        if not self._child_id:
            return False
        progress = s.query(Progress).filter_by(child_id=self._child_id, lesson_id=lesson_id).first()
        return bool(progress and progress.mastered)

    @Slot(int, result="QVariantMap")
    def lesson(self, lesson_id):
        with SessionLocal() as s:
            row = s.get(Lesson, lesson_id)
            if not row:
                return {}
            words = (s.query(Word).filter_by(language=row.language, level=row.level)
                     .order_by(Word.id).limit(12).all())
            audio = s.query(MediaAsset).filter_by(language=row.language, level=row.level, kind="audio").first()
            audio_url = ""
            if audio and audio.path and Path(audio.path).is_file():
                audio_url = QUrl.fromLocalFile(str(Path(audio.path).resolve())).toString()
            return {
                "id": row.id,
                "language": row.language,
                "level": row.level,
                "title": row.title,
                "stageTitle": SKILL_TITLES.get(row.skill, row.skill),
                "skill": row.skill,
                "body": row.body,
                "audioUrl": audio_url,
                "words": [{"text": w.text, "meaning": w.meaning, "example": w.example} for w in words],
            }

    @Slot(int, float, result=bool)
    def completeLesson(self, lesson_id, score=100):
        if not self._child_id:
            return False
        with SessionLocal() as s:
            progress = s.query(Progress).filter_by(child_id=self._child_id, lesson_id=lesson_id).first()
            if not progress:
                progress = Progress(child_id=self._child_id, lesson_id=lesson_id, score=score, mastered=score >= 70)
                s.add(progress)
            else:
                progress.score = max(progress.score, score)
                progress.mastered = progress.mastered or score >= 70
                progress.updated_at = datetime.utcnow()
            s.commit()
        self.refresh()
        return True

    @Slot(result="QVariantList")
    def todayTasks(self):
        with SessionLocal() as s:
            plan = (s.query(DailyPlan).filter_by(child_id=self._child_id)
                    .order_by(DailyPlan.id.desc()).first()) if self._child_id else None
            if plan:
                try:
                    return json.loads(plan.tasks or "[]")
                except Exception:
                    pass
            return [
                {"title": "درس اليوم", "icon": "📚", "done": False},
                {"title": "استمع وتحدث", "icon": "🎧", "done": False},
                {"title": "لعبة الكلمات", "icon": "🎮", "done": False},
            ]

    @Slot(result="QVariantList")
    def stories(self):
        with SessionLocal() as s:
            return [{"id": story.id, "title": story.title, "level": story.level,
                     "language": story.language, "body": story.body}
                    for story in s.query(Story).order_by(Story.level, Story.id).limit(60).all()]

    @Slot(result="QVariantList")
    def achievements(self):
        with SessionLocal() as s:
            earned = ({row.achievement_id for row in
                       s.query(__import__("app.models", fromlist=["ChildAchievement"]).ChildAchievement)
                       .filter_by(child_id=self._child_id).all()} if self._child_id else set())
            return [{"title": item.title, "description": item.description, "earned": item.id in earned}
                    for item in s.query(Achievement).order_by(Achievement.id).all()]

    @Slot(result="QVariantMap")
    def parentReport(self):
        with SessionLocal() as s:
            rows = s.query(Progress).filter_by(child_id=self._child_id).all() if self._child_id else []
            return {
                "lessons": len(rows),
                "mastered": sum(row.mastered for row in rows),
                "average": round(sum(row.score for row in rows) / len(rows), 1) if rows else 0,
                "words": s.query(Word).count(),
            }
