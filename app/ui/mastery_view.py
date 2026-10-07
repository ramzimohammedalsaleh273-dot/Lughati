from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QTableWidget,QTableWidgetItem
from app.services import get_child
from app.mastery import curriculum_progress

class MasteryView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("خريطة الإتقان الحقيقية"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.table=QTableWidget(13,6); self.table.setHorizontalHeaderLabels(["المستوى","الدروس","المكتمل","المتقن","المتوسط","الانتقال"])
        l.addWidget(self.table); self.lang.currentIndexChanged.connect(self.refresh); self.refresh()
    def refresh(self):
        c=get_child()
        rows=curriculum_progress(c.id,self.lang.currentText()) if c else []
        for i,r in enumerate(rows):
            vals=[r["level"],r["lessons"],r["completed"],r["mastered"],r["average"],"جاهز" if r["ready_for_next"] else "يحتاج تدريب"]
            for j,v in enumerate(vals): self.table.setItem(i,j,QTableWidgetItem(str(v)))
