from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QTextEdit
from PySide6.QtMultimedia import QMediaDevices
class SpeakingView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("مختبر التحدث والنطق")); l.addWidget(QLabel("هذه المرحلة توفر تمارين نطق وتسجيل صوتي محلي عند توفر جهاز إدخال صوت.")); self.text=QTextEdit(); self.text.setPlainText("العربية: أنا أتعلم كل يوم.\nEnglish: I learn every day."); l.addWidget(self.text); self.status=QLabel("حالة الميكروفون: "+("متاح" if QMediaDevices.audioInputs() else "غير متاح")); l.addWidget(self.status); b=QPushButton("بدء تمرين التحدث"); b.clicked.connect(lambda:self.status.setText("قل الجملة الظاهرة بوضوح ثم أعد المحاولة.")); l.addWidget(b)
