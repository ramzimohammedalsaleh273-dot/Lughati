from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar
from app.services import get_child,dashboard
class ParentView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); c=get_child(); done,mastered,avg=dashboard(c.id) if c else (0,0,0)
        l.addWidget(QLabel("لوحة ولي الأمر"))
        for title,value in [("الدروس التي بدأها الطفل",done),("الدروس المتقنة",mastered),("متوسط الاختبارات",f"{avg}%")]:
            l.addWidget(QLabel(f"{title}: {value}"))
        bar=QProgressBar(); bar.setRange(0,100); bar.setValue(min(100,mastered*10)); l.addWidget(bar)
