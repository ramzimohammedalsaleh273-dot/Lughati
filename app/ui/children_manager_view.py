from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QListWidget,QLineEdit,QSpinBox,QPushButton,QMessageBox,QInputDialog
from app.services import children
from app.state import set_child
from app.child_manager import create_child,update_child,delete_child
from app.placement import age_group

class ChildrenManagerView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("إدارة الأطفال والملفات التعليمية"))
        self.list=QListWidget(); l.addWidget(self.list)
        form=QHBoxLayout(); self.name=QLineEdit(); self.name.setPlaceholderText("اسم الطفل"); self.age=QSpinBox(); self.age.setRange(4,99); self.age.setValue(6)
        b=QPushButton("إضافة طفل"); b.clicked.connect(self.add_child); form.addWidget(self.name); form.addWidget(self.age); form.addWidget(b); l.addLayout(form)
        row=QHBoxLayout()
        for title,fn in [("اختيار الحالي",self.select),("تعديل",self.edit),("حذف",self.remove)]:
            b=QPushButton(title); b.clicked.connect(fn); row.addWidget(b)
        l.addLayout(row); self.info=QLabel(); l.addWidget(self.info); self.refresh()
    def refresh(self):
        self.list.clear()
        for c in children(): self.list.addItem(f"{c.id} — {c.name} — {c.age} سنة — الفئة {age_group(c.age)}")
    def selected_id(self):
        item=self.list.currentItem()
        return int(item.text().split("—",1)[0].strip()) if item else None
    def add_child(self):
        try: cid=create_child(self.name.text(),self.age.value()); set_child(cid); self.name.clear(); self.refresh()
        except Exception as e: QMessageBox.warning(self,"تنبيه",str(e))
    def select(self):
        cid=self.selected_id()
        if cid: set_child(cid); self.info.setText("تم اختيار الطفل الحالي.")
    def edit(self):
        cid=self.selected_id()
        if not cid:return
        name,ok=QInputDialog.getText(self,"تعديل الطفل","الاسم الجديد:")
        if not ok:return
        try:update_child(cid,name=name); self.refresh()
        except Exception as e:QMessageBox.warning(self,"تنبيه",str(e))
    def remove(self):
        cid=self.selected_id()
        if not cid:return
        if QMessageBox.question(self,"تأكيد الحذف","سيتم حذف بيانات هذا الطفل التعليمية. هل أنت متأكد؟")==QMessageBox.StandardButton.Yes:
            delete_child(cid); self.refresh()
