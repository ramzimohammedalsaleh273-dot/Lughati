from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar,QPushButton,QFileDialog,QMessageBox
from app.services import get_child,dashboard
from app.reports import export_child_report
class ParentView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); c=get_child(); done,mastered,avg=dashboard(c.id) if c else (0,0,0)
        l.addWidget(QLabel("لوحة ولي الأمر"))
        for title,value in [("الدروس التي بدأها الطفل",done),("الدروس المتقنة",mastered),("متوسط الاختبارات",f"{avg}%")]:
            l.addWidget(QLabel(f"{title}: {value}"))
        bar=QProgressBar(); bar.setRange(0,100); bar.setValue(min(100,mastered*10)); l.addWidget(bar)
        b=QPushButton("تصدير تقرير الطفل"); b.clicked.connect(self.export_report); l.addWidget(b)
    def export_report(self):
        c=get_child()
        if not c:return
        path,_=QFileDialog.getSaveFileName(self,"حفظ التقرير","","CSV (*.csv)")
        if path:
            try: export_child_report(c.id,path); QMessageBox.information(self,"تم","تم حفظ التقرير.")
            except Exception as e: QMessageBox.critical(self,"فشل",str(e))
