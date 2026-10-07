from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar
from app.services import get_child,dashboard
from app.analytics import snapshot
class ProgressView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); self.refresh()
    def refresh(self):
        while self.layout().count():
            item=self.layout().takeAt(0); w=item.widget()
            if w: w.deleteLater()
        c=get_child()
        if not c: return
        done,mastered,avg=dashboard(c.id); data=snapshot(c.id)
        self.layout().addWidget(QLabel(f"تقدم {c.name}"))
        for title,val in [("الدروس التي بدأت",done),("الدروس المتقنة",mastered),("متوسط الاختبارات",avg)]:
            self.layout().addWidget(QLabel(f"{title}: {val}")); b=QProgressBar(); b.setRange(0,100); b.setValue(int(val) if title=="متوسط الاختبارات" else min(100,int(val*100/max(1,done)))); self.layout().addWidget(b)
        for lang,val in data["languages"].items(): self.layout().addWidget(QLabel(f"متوسط {lang}: {val}%"))
        for skill,val in data["skills"].items(): self.layout().addWidget(QLabel(f"المهارة {skill}: {val}%"))