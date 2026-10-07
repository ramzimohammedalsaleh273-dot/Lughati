from pathlib import Path
from PySide6.QtWidgets import QWidget,QVBoxLayout,QPushButton,QFileDialog,QLabel,QSlider
from PySide6.QtCore import QUrl,Qt
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

class MediaPlayerView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self)
        self.label=QLabel("مشغل الوسائط المحلي — يعمل دون إنترنت")
        l.addWidget(self.label)
        self.video=QVideoWidget(); l.addWidget(self.video)
        self.player=QMediaPlayer(self); self.audio=QAudioOutput(self); self.player.setAudioOutput(self.audio); self.player.setVideoOutput(self.video)
        b=QPushButton("فتح ملف صوت أو فيديو"); b.clicked.connect(self.open_file); l.addWidget(b)
        play=QPushButton("تشغيل / إيقاف"); play.clicked.connect(self.toggle); l.addWidget(play)
        self.slider=QSlider(Qt.Horizontal); self.slider.setRange(0,0); l.addWidget(self.slider)
        self.player.durationChanged.connect(lambda x:self.slider.setRange(0,int(x)))
        self.player.positionChanged.connect(lambda x:self.slider.setValue(int(x)))
        self.slider.sliderMoved.connect(lambda x:self.player.setPosition(int(x)))
    def open_file(self):
        p,_=QFileDialog.getOpenFileName(self,"اختيار وسائط","","الوسائط (*.mp3 *.wav *.ogg *.mp4 *.m4a *.webm)")
        if p: self.player.setSource(QUrl.fromLocalFile(p)); self.player.play(); self.label.setText(Path(p).name)
    def toggle(self):
        self.player.pause() if self.player.playbackState()==QMediaPlayer.PlayingState else self.player.play()
