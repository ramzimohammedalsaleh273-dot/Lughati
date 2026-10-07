from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QProgressBar,QPushButton,QFileDialog,QMessageBox,QInputDialog
from app.services import get_child,dashboard
from app.reports import export_child_report
from app.auth import verify_parent_pin,set_parent_pin,parent_pin_enabled

class ParentView(QWidget):
    def __init__(self):
        super().__init__(); self.layout=QVBoxLayout(self); self.unlocked=False; self.refresh()
    def clear(self):
        while self.layout.count():
            item=self.layout.takeAt(0); w=item.widget()
            if w:w.deleteLater()
    def refresh(self):
        self.clear(); self.layout.addWidget(QLabel("لوحة ولي الأمر"))
        if parent_pin_enabled() and not self.unlocked:
            self.layout.addWidget(QLabel("لوحة ولي الأمر محمية برمز."))
            b=QPushButton("فتح اللوحة"); b.clicked.connect(self.unlock); self.layout.addWidget(b)
            s=QPushButton("تعيين رمز جديد"); s.clicked.connect(self.change_pin); self.layout.addWidget(s); return
        c=get_child()
        if not c:self.layout.addWidget(QLabel("لا يوجد طفل.")); return
        done,mastered,avg=dashboard(c.id)
        for title,value in [("الدروس التي بدأها",done),("الدروس المتقنة",mastered),("متوسط الاختبارات",f"{avg}%")]:
            self.layout.addWidget(QLabel(f"{title}: {value}"))
        bar=QProgressBar(); bar.setRange(0,100); bar.setValue(min(100,mastered*10)); self.layout.addWidget(bar)
        report=QPushButton("تصدير تقرير الطفل"); report.clicked.connect(self.export_report); self.layout.addWidget(report)
        pin=QPushButton("تغيير رمز ولي الأمر"); pin.clicked.connect(self.change_pin); self.layout.addWidget(pin)
    def unlock(self):
        value,ok=QInputDialog.getText(self,"حماية ولي الأمر","أدخل الرمز:")
        if ok and verify_parent_pin(value): self.unlocked=True; self.refresh()
        elif ok: QMessageBox.warning(self,"رفض","الرمز غير صحيح.")
    def change_pin(self):
        value,ok=QInputDialog.getText(self,"رمز ولي الأمر","أدخل رمزاً جديداً (4 أرقام أو أكثر):")
        if ok:
            try:set_parent_pin(value); self.unlocked=True; QMessageBox.information(self,"تم","تم حفظ الرمز محلياً."); self.refresh()
            except Exception as e: QMessageBox.warning(self,"تنبيه",str(e))
    def export_report(self):
        c=get_child()
        if not c:return
        path,_=QFileDialog.getSaveFileName(self,"حفظ التقرير","","CSV (*.csv)")
        if path:
            try:export_child_report(c.id,path); QMessageBox.information(self,"تم","تم حفظ التقرير.")
            except Exception as e:QMessageBox.critical(self,"فشل",str(e))
