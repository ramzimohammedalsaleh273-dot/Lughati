from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton,QSpinBox
from app.database import SessionLocal
from app.models import Child
class ChildView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("ملف الطفل")); self.name=QLineEdit(); self.name.setPlaceholderText("اسم الطفل"); l.addWidget(self.name); self.age=QSpinBox(); self.age.setRange(3,18); self.age.setValue(6); l.addWidget(self.age); b=QPushButton("حفظ الملف"); b.clicked.connect(self.save); l.addWidget(b); self.msg=QLabel(); l.addWidget(self.msg)
    def save(self):
        with SessionLocal() as s:
            c=s.query(Child).first()
            if not c: c=Child(); s.add(c)
            c.name=self.name.text().strip() or "الطفل"; c.age=self.age.value(); s.commit()
        self.msg.setText("✓ تم حفظ الملف محليًا.")
