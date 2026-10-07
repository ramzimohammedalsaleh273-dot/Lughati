from pathlib import Path
from datetime import datetime
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,QFileDialog,QMessageBox
from PySide6.QtMultimedia import QAudioInput,QMediaCaptureSession,QMediaRecorder,QMediaPlayer,QAudioOutput
from PySide6.QtMultimedia import QMediaFormat

class SpeakingView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); l=self.layout()
        l.addWidget(QLabel("مختبر التحدث والنطق"))
        self.prompt=QLineEdit(); self.prompt.setPlaceholderText("اكتب الجملة التي تريد قراءتها بصوتك"); l.addWidget(self.prompt)
        row=QHBoxLayout(); self.start=QPushButton("بدء التسجيل"); self.stop=QPushButton("إيقاف التسجيل"); self.play=QPushButton("تشغيل التسجيل"); row.addWidget(self.start); row.addWidget(self.stop); row.addWidget(self.play); l.addLayout(row)
        self.status=QLabel("جاهز"); l.addWidget(self.status)
        self.player=QMediaPlayer(self); self.output=QAudioOutput(self); self.player.setAudioOutput(self.output)
        self.audio_input=QAudioInput(self); self.capture=QMediaCaptureSession(self); self.capture.setAudioInput(self.audio_input); self.recorder=QMediaRecorder(self); self.capture.setRecorder(self.recorder)
        self.path=None
        self.start.clicked.connect(self.record); self.stop.clicked.connect(self.stop_record); self.play.clicked.connect(self.play_record)
    def record(self):
        Path("data/recordings").mkdir(parents=True,exist_ok=True)
        self.path=Path("data/recordings")/(datetime.now().strftime("%Y%m%d_%H%M%S")+".wav")
        self.recorder.setOutputLocation(QUrl.fromLocalFile(str(self.path.resolve())))
        self.recorder.record(); self.status.setText("جاري التسجيل… تحدث الآن.")
    def stop_record(self):
        self.recorder.stop(); self.status.setText(f"تم حفظ التسجيل: {self.path}" if self.path else "لا يوجد تسجيل")
    def play_record(self):
        if not self.path or not self.path.exists(): QMessageBox.information(self,"تنبيه","سجل صوتاً أولاً."); return
        self.player.setSource(QUrl.fromLocalFile(str(self.path.resolve()))); self.player.play(); self.status.setText("تشغيل التسجيل")
