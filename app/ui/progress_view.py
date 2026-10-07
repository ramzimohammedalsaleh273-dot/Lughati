from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar
from app.services import get_child,dashboard
class ProgressView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); c=get_child(); done,mastered,avg=dashboard(c.id) if c else (0,0,0); l.addWidget(QLabel("تقدم التعلم")); 
        for title,val in [("الدروس التي بدأت",done),("الدروس المتقنة",mastered),("متوسط الاختبارات",avg)]:
            l.addWidget(QLabel(f"{title}: {val}")); b=QProgressBar(); b.setRange(0,100); b.setValue(int(val) if title=="متوسط الاختبارات" else min(100,int(val*10))); l.addWidget(b)
