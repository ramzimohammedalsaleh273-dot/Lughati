from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QListWidget,QPushButton
from app.services import lessons,get_child,save_lesson
class PlanView(QWidget):
    def __init__(self):
        super().__init__(); self.data=lessons("ar")+lessons("en"); l=QVBoxLayout(self); l.addWidget(QLabel("خطة التعلم اليومية")); self.list=QListWidget(); l.addWidget(self.list); b=QPushButton("فتح/إتمام الدرس المحدد"); b.clicked.connect(self.complete); l.addWidget(b); self.refresh()
    def refresh(self): self.list.clear(); self.list.addItems([f"{x.language.upper()} | المستوى {x.level} | {x.title}" for x in self.data])
    def complete(self):
        i=self.list.currentRow()
        if i>=0: save_lesson(get_child().id,self.data[i].id,100); self.list.item(i).setText(self.list.item(i).text()+" ✓")
