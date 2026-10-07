from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QProgressBar
from app.services import get_child
from app.skill_engine import report,readiness

class SkillDashboardView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("لوحة المهارات والإتقان"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.info=QLabel(); l.addWidget(self.info)
        self.bars={}; self.labels={}
        for skill in ("listening","speaking","reading","writing","vocabulary","grammar"):
            label=QLabel(skill); bar=QProgressBar(); bar.setRange(0,100); self.labels[skill]=label; self.bars[skill]=bar; l.addWidget(label); l.addWidget(bar)
        self.lang.currentIndexChanged.connect(self.refresh); self.refresh()
    def refresh(self):
        c=get_child()
        if not c:return
        rows=report(c.id,self.lang.currentText()); r=readiness(c.id,self.lang.currentText())
        self.info.setText(f"المستوى الحالي: {r['current_level']} | متوسط المهارات: {r['skill_average']}% | يحتاج تدريب: {', '.join(r['weakest'])}")
        for x in rows:self.labels[x.skill].setText(f"{x.skill} — {x.level}"); self.bars[x.skill].setValue(int(x.score))
