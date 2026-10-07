from PySide6.QtWidgets import QWidget,QVBoxLayout,QListWidget,QLabel
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Achievement,ChildAchievement
from app.services import get_child

class AchievementsView(QWidget):
    def __init__(self):
        super().__init__(); layout=QVBoxLayout(self); layout.addWidget(QLabel("الإنجازات والشارات")); self.list=QListWidget(); layout.addWidget(self.list); self.refresh()
    def refresh(self):
        child=get_child(); self.list.clear()
        if not child:return
        with SessionLocal() as s:
            earned={x.achievement_id for x in s.scalars(select(ChildAchievement).where(ChildAchievement.child_id==child.id)).all()}
            for a in s.scalars(select(Achievement).order_by(Achievement.id)).all(): self.list.addItem(("🏆 " if a.id in earned else "🔒 ")+a.title+" — "+a.description)
