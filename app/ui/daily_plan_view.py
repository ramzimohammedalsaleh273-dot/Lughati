from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QSpinBox,QPushButton,QListWidget,QMessageBox
from app.services import get_child,complete_daily_plan
from app.daily_plan import build_plan,get_or_create_plan

class DailyPlanView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("الخطة الذكية لليوم"))
        row=QHBoxLayout(); self.lang=QComboBox(); self.lang.addItems(["ar","en"]); self.minutes=QSpinBox(); self.minutes.setRange(10,120); self.minutes.setValue(20); row.addWidget(self.lang); row.addWidget(self.minutes); l.addLayout(row)
        self.make=QPushButton("إنشاء الخطة"); self.make.clicked.connect(self.refresh); l.addWidget(self.make)
        self.list=QListWidget(); l.addWidget(self.list)
        self.done=QPushButton("إنهاء خطة اليوم"); self.done.clicked.connect(self.complete); l.addWidget(self.done)
        self.info=QLabel(); l.addWidget(self.info); self.refresh()
    def refresh(self):
        self.list.clear(); c=get_child()
        if not c: return
        get_or_create_plan(c.id,self.lang.currentText(),self.minutes.value())
        tasks=build_plan(c.id,self.lang.currentText(),self.minutes.value())
        for t in tasks:self.list.addItem(f"{t.minutes} دقائق — {t.title}")
        self.info.setText(f"عدد الأنشطة: {len(tasks)}")
    def complete(self):
        c=get_child()
        if not c: return
        complete_daily_plan(c.id,self.lang.currentText()); QMessageBox.information(self,"تم","تم تسجيل إكمال خطة اليوم.")
