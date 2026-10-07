from PySide6.QtWidgets import QWidget,QVBoxLayout,QComboBox,QListWidget,QTextEdit
from app.services import stories

class StoriesLibraryView(QWidget):
    def __init__(self):
        super().__init__(); layout=QVBoxLayout(self)
        self.language=QComboBox(); self.language.addItems(["ar","en"]); layout.addWidget(self.language)
        self.list=QListWidget(); layout.addWidget(self.list)
        self.text=QTextEdit(); self.text.setReadOnly(True); layout.addWidget(self.text)
        self.language.currentTextChanged.connect(self.refresh); self.list.currentRowChanged.connect(self.show_story)
        self.data=[]; self.refresh()
    def refresh(self):
        self.data=stories(self.language.currentText()); self.list.clear(); self.list.addItems([f"المستوى {x.level} — {x.title}" for x in self.data]); self.show_story(0)
    def show_story(self,index):
        self.text.setPlainText(self.data[index].body if 0<=index<len(self.data) else "لا توجد قصص بعد")
