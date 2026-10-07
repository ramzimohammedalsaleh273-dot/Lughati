from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar,QComboBox
from app.services import get_child
from app.learning import skill_report

class SkillsView(QWidget):
 def __init__(self):
  super().__init__(); self.l=QVBoxLayout(self); self.l.addWidget(QLabel("تقييم المهارات")); self.lang=QComboBox(); self.lang.addItems(["ar","en"]); self.l.addWidget(self.lang); self.lang.currentIndexChanged.connect(self.refresh); self.refresh()
 def refresh(self):
  while self.l.count()>2:
   item=self.l.takeAt(2); w=item.widget()
   if w:w.deleteLater()
  c=get_child(); report=skill_report(c.id,self.lang.currentText()) if c else {}
  for skill in ["listening","speaking","reading","writing","vocabulary","grammar"]:
   val=report.get(skill,0); self.l.addWidget(QLabel(f"{skill}: {val}%")); b=QProgressBar(); b.setRange(0,100); b.setValue(int(val)); self.l.addWidget(b)
