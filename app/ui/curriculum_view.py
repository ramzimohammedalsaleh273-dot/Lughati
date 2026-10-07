from PySide6.QtWidgets import QWidget,QVBoxLayout,QComboBox,QListWidget,QTextEdit
from app.services import lessons

class CurriculumView(QWidget):
    def __init__(self):
        super().__init__()
        layout=QVBoxLayout(self)
        self.language=QComboBox(); self.language.addItems(["ar","en"])
        self.level=QComboBox(); self.level.addItems([str(i) for i in range(13)])
        self.list=QListWidget(); self.body=QTextEdit(); self.body.setReadOnly(True)
        layout.addWidget(self.language); layout.addWidget(self.level); layout.addWidget(self.list); layout.addWidget(self.body)
        self.language.currentTextChanged.connect(self.refresh); self.level.currentTextChanged.connect(self.refresh); self.list.currentRowChanged.connect(self.show_item)
        self.data=[]; self.refresh()
    def refresh(self):
        self.data=lessons(self.language.currentText(),int(self.level.currentText())); self.list.clear(); self.list.addItems([x.title for x in self.data]); self.show_item(0)
    def show_item(self,index):
        self.body.setPlainText(self.data[index].body if 0<=index<len(self.data) else "لا توجد دروس")
