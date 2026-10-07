from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar
from app.services import get_child
from app.learning import skill_report
class SkillsView(QWidget):
 def __init__(self):
  super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("تقييم المهارات")); c=get_child(); report=skill_report(c.id) if c else {}
  for skill in ["listening","speaking","reading","writing","vocabulary","grammar","placement"]:
   val=report.get(skill,0); l.addWidget(QLabel(f"{skill}: {val}%")); b=QProgressBar(); b.setValue(int(val)); l.addWidget(b)
