from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QGridLayout,QFrame
from app.services import get_child,dashboard
from app.achievements import summary

class DashboardView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout())
        self.refresh()
    def refresh(self):
        while self.layout().count():
            item=self.layout().takeAt(0); w=item.widget()
            if w: w.deleteLater()
        child=get_child(); d=dashboard(child.id); a=summary(child.id)
        title=QLabel(f"مرحباً {child.name} — لوحة التعلم")
        title.setStyleSheet("font-size:24px;font-weight:bold")
        self.layout().addWidget(title)
        g=QGridLayout()
        vals=[("الدروس المكتملة",a["lessons_mastered"]),("الاختبارات",a["tests"]),("متوسط الاختبارات",f'{a["test_average"]}%'),("متوسط التقدم",f'{d.get("mastery",0)}%')]
        for i,(k,v) in enumerate(vals):
            f=QFrame(); f.setFrameShape(QFrame.StyledPanel); l=QVBoxLayout(f); l.addWidget(QLabel(k)); l.addWidget(QLabel(str(v))); g.addWidget(f,i//2,i%2)
        self.layout().addLayout(g)
