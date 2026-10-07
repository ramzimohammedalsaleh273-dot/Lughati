from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QListWidget,QListWidgetItem
from app.services import words
class WordsView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("قاموس الكلمات")); self.list=QListWidget(); l.addWidget(self.list)
        for lang in ("ar","en"):
            self.list.addItem("— العربية —" if lang=="ar" else "— English —")
            for w in words(lang): self.list.addItem(QListWidgetItem(f"{w.text}  —  {w.meaning}\n{w.example}"))
