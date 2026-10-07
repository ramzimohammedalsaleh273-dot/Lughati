from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QTableWidget,QTableWidgetItem
from app.services import children
from app.progress_engine import snapshot

class ParentReportView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("تقرير ولي الأمر متعدد الأطفال")); self.child=QComboBox(); l.addWidget(self.child); self.table=QTableWidget(0,4); self.table.setHorizontalHeaderLabels(["اللغة","الإكمال","الإتقان","الاختبارات"]); l.addWidget(self.table); self.child.currentIndexChanged.connect(self.refresh); self.load()
    def load(self):
        self.child.clear()
        for c in children():self.child.addItem(f"{c.name} — {c.age} سنة",c.id)
        self.refresh()
    def refresh(self):
        cid=self.child.currentData()
        if cid is None:return
        self.table.setRowCount(2)
        for i,lang in enumerate(("ar","en")):
            r=snapshot(cid,lang)
            vals=[lang,f"{r['completion']}%",f"{r['mastery']}%",r["tests"]]
            for j,v in enumerate(vals):self.table.setItem(i,j,QTableWidgetItem(str(v)))
