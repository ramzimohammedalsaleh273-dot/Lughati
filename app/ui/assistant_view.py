from PySide6.QtWidgets import QWidget,QVBoxLayout,QLineEdit,QPushButton,QTextEdit,QComboBox
from app.assistant import answer

class AssistantView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); l=self.layout()
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.input=QLineEdit(); self.input.setPlaceholderText("اسأل عن درس أو كلمة أو مراجعة"); l.addWidget(self.input)
        self.ask=QPushButton("اسأل"); self.ask.clicked.connect(self.run); l.addWidget(self.ask)
        self.out=QTextEdit(); self.out.setReadOnly(True); l.addWidget(self.out)
    def run(self):
        self.out.setPlainText(answer(self.input.text(),self.lang.currentText()))
