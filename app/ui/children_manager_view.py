from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QListWidget,QLineEdit,QSpinBox,QPushButton,QMessageBox
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Child
from app.placement import age_group

class ChildrenManagerView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); self.list=QListWidget(); l.addWidget(self.list)
        row=QHBoxLayout(); self.name=QLineEdit(); self.name.setPlaceholderText("اسم الطفل"); self.age=QSpinBox(); self.age.setRange(2,18); self.age.setValue(6); add=QPushButton("إضافة طفل"); add.clicked.connect(self.add); row.addWidget(self.name); row.addWidget(self.age); row.addWidget(add); l.addLayout(row); self.refresh()
    def refresh(self):
        self.list.clear()
        with SessionLocal() as s:
            for c in s.scalars(select(Child).order_by(Child.id)).all(): self.list.addItem(f"{c.id} — {c.name} — {c.age} سنة — الفئة {age_group(c.age)}")
    def add(self):
        n=self.name.text().strip()
        if not n: QMessageBox.warning(self,"تنبيه","اكتب اسم الطفل."); return
        with SessionLocal() as s: s.add(Child(name=n,age=self.age.value())); s.commit()
        self.name.clear(); self.refresh()
