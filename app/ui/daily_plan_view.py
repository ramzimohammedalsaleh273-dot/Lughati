from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QSpinBox,QPushButton
from app.services import get_child,create_daily_plan

class DailyPlanView(QWidget):
    def __init__(self):
        super().__init__(); layout=QVBoxLayout(self); layout.addWidget(QLabel("الخطة اليومية الذكية")); self.language=QComboBox(); self.language.addItems(["ar","en"]); layout.addWidget(self.language); self.minutes=QSpinBox(); self.minutes.setRange(5,180); self.minutes.setValue(20); layout.addWidget(self.minutes); b=QPushButton("إنشاء خطة اليوم"); b.clicked.connect(self.create); layout.addWidget(b); self.out=QLabel(); layout.addWidget(self.out)
    def create(self):
        child=get_child()
        if child:
            p=create_daily_plan(child.id,self.language.currentText(),self.minutes.value()); self.out.setText(f"✓ خطة {p.date}: {p.minutes} دقيقة — اللغة {p.language}")
