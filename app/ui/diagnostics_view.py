from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QPlainTextEdit
from app.validation import full_check

class DiagnosticsView(QWidget):
    def __init__(self):
        super().__init__()
        l=QVBoxLayout(self)
        l.addWidget(QLabel("تشخيص النظام وجودة المحتوى"))
        self.run=QPushButton("فحص شامل")
        self.run.clicked.connect(self.check)
        l.addWidget(self.run)
        self.out=QPlainTextEdit()
        self.out.setReadOnly(True)
        l.addWidget(self.out)
        self.check()

    def check(self):
        r=full_check()
        self.out.setPlainText(str(r)+"\nالحالة: "+("سليم" if r["ok"] else "يحتاج إصلاح"))
