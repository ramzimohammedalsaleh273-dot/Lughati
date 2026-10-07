from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton,QTextEdit
from app.assistant import answer
class HelpView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("مساعد لغتي"))
        self.query=QLineEdit(); l.addWidget(self.query)
        b=QPushButton("اسأل"); b.clicked.connect(self.ask); l.addWidget(b)
        self.out=QTextEdit(); self.out.setReadOnly(True); l.addWidget(self.out)
    def ask(self): self.out.setPlainText(answer(self.query.text(),"ar"))
