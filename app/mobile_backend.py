from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QObject, Signal, Slot, Property
from app.database import SessionLocal
from app.models import Child, Lesson, Progress, Word, Story, Achievement, DailyPlan

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
            self._xp = 0; self._streak = 0; self._mastered = 0; self._completed = 0
            return
        rows = s.query(Progress).filter_by(child_id=self._child_id).all()
        self._completed = len(rows)
        self._mastered = sum(1 for r in rows if r.mastered)
        self._xp = int(sum(max(0, r.score) for r in rows) * 10)
        self._streak = 1 if rows else 0

    @Property(str, notify=changed)
    def childName(self): return self._child_name

    @Property(int, notify=changed)
    def childAge(self): return self._age

    @Property(int, notify=changed)
    def xp(self): return self._xp

    @Property(int, notify=changed)
    def completedLessons(self): return self._completed

    @Property(int, notify=changed)
    def masteredLessons(self): return self._mastered

    @Property(int, notify=changed)
    def streak(self): return self._streak

    @Slot(result="QVariantList")
    def levels(self):
        result=[]
        with SessionLocal() as s:
            for level in range(13):
                ar=s.query(Lesson).filter_by(language="ar",level=level).count()
                en=s.query(Lesson).filter_by(language="en",level=level).count()
                result.append({"level":level,"title":f"المستوى {level}","ar":ar,"en":en,"locked":False})
        return result

    @Slot(int, result="QVariantList")
    def lessons(self, level):
        result=[]
        with SessionLocal() as s:
            for row in s.query(Lesson).filter_by(level=level).order_by(Lesson.language,Lesson.id).all():
                result.append({"id":row.id,"language":row.language,"title":row.title,"skill":row.skill,"body":row.body,"done":self._lesson_done(s,row.id)})
        return result

    def _lesson_done(self,s,lesson_id):
        if not self._child_id: return False
        p=s.query(Progress).filter_by(child_id=self._child_id,lesson_id=lesson_id).first()
        return bool(p and p.mastered)

    @Slot(int, result="QVariantMap")
    def lesson(self, lesson_id):
        with SessionLocal() as s:
            row=s.get(Lesson,lesson_id)
            if not row: return {}
            words=s.query(Word).filter_by(language=row.language,level=row.level).limit(6).all()
            return {"id":row.id,"language":row.language,"title":row.title,"skill":row.skill,"body":row.body,
                    "words":[{"text":w.text,"meaning":w.meaning,"example":w.example} for w in words]}

    @Slot(int, float, result=bool)
    def completeLesson(self, lesson_id, score=100):
        if not self._child_id: return False
        with SessionLocal() as s:
            p=s.query(Progress).filter_by(child_id=self._child_id,lesson_id=lesson_id).first()
            if not p:
                p=Progress(child_id=self._child_id,lesson_id=lesson_id,score=score,mastered=score>=70)
                s.add(p)
            else:
                p.score=max(p.score,score); p.mastered=p.mastered or score>=70; p.updated_at=datetime.utcnow()
            s.commit()
        self.refresh()
        return True

    @Slot(result="QVariantList")
    def todayTasks(self):
        with SessionLocal() as s:
            plan=s.query(DailyPlan).filter_by(child_id=self._child_id).order_by(DailyPlan.id.desc()).first() if self._child_id else None
            if plan:
                try: return json.loads(plan.tasks or "[]")
                except Exception: pass
            return [
                {"title":"درس اليوم","icon":"📚","done":False},
                {"title":"استمع وتحدث","icon":"🎧","done":False},
                {"title":"لعبة الكلمات","icon":"🎮","done":False},
            ]

    @Slot(result="QVariantList")
    def stories(self):
        with SessionLocal() as s:
            return [{"id":x.id,"title":x.title,"level":x.level,"language":x.language,"body":x.body}
                    for x in s.query(Story).order_by(Story.level,Story.id).limit(60).all()]

    @Slot(result="QVariantList")
    def achievements(self):
        with SessionLocal() as s:
            earned={x.achievement_id for x in s.query(__import__("app.models",fromlist=["ChildAchievement"]).ChildAchievement).filter_by(child_id=self._child_id).all()} if self._child_id else set()
            return [{"title":x.title,"description":x.description,"earned":x.id in earned}
                    for x in s.query(Achievement).order_by(Achievement.id).all()]

    @Slot(result="QVariantMap")
    def parentReport(self):
        with SessionLocal() as s:
            rows=s.query(Progress).filter_by(child_id=self._child_id).all() if self._child_id else []
            return {"lessons":len(rows),"mastered":sum(r.mastered for r in rows),
                    "average":round(sum(r.score for r in rows)/len(rows),1) if rows else 0,
                    "words":s.query(Word).count()}
