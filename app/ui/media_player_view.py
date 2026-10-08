from pathlib import Path
from PySide6.QtCore import QUrl,Qt
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QFileDialog,QSlider
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
class MediaPlayerView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); l=self.layout()
        self.info=QLabel("لم يتم اختيار ملف"); l.addWidget(self.info)
        row=QHBoxLayout(); self.open=QPushButton("فتح ملف"); self.play=QPushButton("تشغيل/إيقاف"); row.addWidget(self.open); row.addWidget(self.play); l.addLayout(row)
        self.video=QVideoWidget(); l.addWidget(self.video,1); self.slider=QSlider(Qt.Horizontal); l.addWidget(self.slider)
        self.player=QMediaPlayer(self); self.audio=QAudioOutput(self); self.player.setAudioOutput(self.audio); self.player.setVideoOutput(self.video)
        self.open.clicked.connect(self.open_file); self.play.clicked.connect(self.toggle); self.slider.sliderMoved.connect(self.player.setPosition); self.player.positionChanged.connect(self.slider.setValue); self.player.durationChanged.connect(self.slider.setMaximum)
    def set_media(self,path,title=None):
        p=Path(path)
        if not p.exists(): return False
        self.player.setSource(QUrl.fromLocalFile(str(p.resolve()))); self.info.setText(title or p.name); self.player.play(); return True
    def open_file(self):
        path,_=QFileDialog.getOpenFileName(self,"اختيار ملف وسائط","","وسائط (*.mp3 *.wav *.ogg *.m4a *.mp4 *.webm *.mkv *.avi *.mov)")
        if path:self.set_media(path,path)
    def toggle(self):
        if self.player.isPlaying(): self.player.pause()
        else: self.player.play()
