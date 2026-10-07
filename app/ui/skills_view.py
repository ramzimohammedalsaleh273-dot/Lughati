from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar,QComboBox
from app.services import get_child
from app.skill_engine import report,readiness

class SkillsView(QWidget):
    def __init__(self):
        super().__init__(); self.l=QVBoxLayout(self); self.l.addWidget(QLabel("تقييم المهارات الست")); self.lang=QComboBox(); self.lang.addItems(["ar","en"]); self.l.addWidget(self.lang); self.info=QLabel(); self.l.addWidget(self.info); self.bars={}; self.labels={}
        for skill in ("listening","speaking","reading","writing","vocabulary","grammar"):
            self.labels[skill]=QLabel(skill); self.bars[skill]=QProgressBar(); self.bars[skill].setRange(0,100); self.l.addWidget(self.labels[skill]); self.l.addWidget(self.bars[skill])
        self.lang.currentIndexChanged.connect(self.refresh); self.refresh()
    def refresh(self):
        c=get_child()
        if not c:return
        rows=report(c.id,self.lang.currentText()); r=readiness(c.id,self.lang.currentText())
        self.info.setText(f"المستوى الحالي: {r['current_level']} | متوسط المهارات: {r['skill_average']}% | أضعف مهارتين: {', '.join(r['weakest'])}")
        for x in rows:self.labels[x.skill].setText(f"{x.skill} — {x.level}"); self.bars[x.skill].setValue(int(x.score))
