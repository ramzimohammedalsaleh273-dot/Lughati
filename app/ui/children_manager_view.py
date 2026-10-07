from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QListWidget,QLineEdit,QSpinBox,QPushButton,QMessageBox
from app.services import children
from app.state import set_child,subscribe
from app.models import Child
from app.database import SessionLocal
from app.placement import age_group

class ChildrenManagerView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("إدارة الأطفال والملفات التعليمية"))
        self.list=QListWidget(); l.addWidget(self.list)
        form=QHBoxLayout(); self.name=QLineEdit(); self.name.setPlaceholderText("اسم الطفل"); self.age=QSpinBox(); self.age.setRange(4,99); self.age.setValue(6); add=QPushButton("إضافة طفل"); add.clicked.connect(self.add_child); form.addWidget(self.name); form.addWidget(self.age); form.addWidget(add); l.addLayout(form)
        self.select_btn=QPushButton("اختيار الطفل الحالي"); self.select_btn.clicked.connect(self.select); l.addWidget(self.select_btn)
        self.info=QLabel(); l.addWidget(self.info); self.refresh()
    def refresh(self):
        self.list.clear()
        for c in children(): self.list.addItem(f"{c.id} — {c.name} — {c.age} سنة — الفئة {age_group(c.age)}")
    def add_child(self):
        name=self.name.text().strip()
        if not name: QMessageBox.warning(self,"تنبيه","اكتب اسم الطفل."); return
        with SessionLocal() as s:
            c=Child(name=name,age=self.age.value()); s.add(c); s.commit(); cid=c.id
        set_child(cid); self.name.clear(); self.refresh()
    def select(self):
        row=self.list.currentRow(); data=children()
        if row<0 or row>=len(data): return
        set_child(data[row].id); self.info.setText(f"تم اختيار: {data[row].name}"); self.refresh()
