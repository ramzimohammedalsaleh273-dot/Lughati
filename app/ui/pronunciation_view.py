from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton,QTextEdit
from app.pronunciation_engine import score_pronunciation
class PronunciationView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self)
        l.addWidget(QLabel("مختبر النطق — أدخل النص الهدف ثم نتيجة التعرف/محاولتك للمقارنة"))
        self.target=QLineEdit(); self.target.setPlaceholderText("النص الهدف"); l.addWidget(self.target)
        self.attempt=QLineEdit(); self.attempt.setPlaceholderText("ما نطقته/النص المتعرف عليه"); l.addWidget(self.attempt)
        b=QPushButton("حلّل المحاولة"); b.clicked.connect(self.analyze); l.addWidget(b)
        self.out=QTextEdit(); self.out.setReadOnly(True); l.addWidget(self.out)
    def analyze(self):
        r=score_pronunciation(self.target.text(),self.attempt.text())
        self.out.setPlainText(f"النتيجة: {r['score']}%\nالتقييم: {r['level']}\n{r['feedback']}")
