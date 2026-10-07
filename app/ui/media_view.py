from pathlib import Path
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QListWidget,QPushButton,QFileDialog,QMessageBox,QComboBox,QSpinBox
from app.config import MEDIA_DIR
from app.database import SessionLocal
from app.models import MediaAsset

class MediaView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("مكتبة الصوت والفيديو المحلية"))
        row=QHBoxLayout(); self.lang=QComboBox(); self.lang.addItems(["ar","en"]); self.level=QSpinBox(); self.level.setRange(0,12); self.kind=QComboBox(); self.kind.addItems(["audio","video"]); row.addWidget(self.lang); row.addWidget(self.level); row.addWidget(self.kind); l.addLayout(row)
        self.list=QListWidget(); l.addWidget(self.list)
        add=QPushButton("إضافة ملف وسائط مرخص"); add.clicked.connect(self.add_media); l.addWidget(add)
        self.refresh()
    def refresh(self):
        self.list.clear()
        with SessionLocal() as s:
            rows=list(s.query(MediaAsset).filter_by(language=self.lang.currentText(),level=self.level.value(),kind=self.kind.currentText()).order_by(MediaAsset.id).all())
        for r in rows:self.list.addItem(f"{r.title} — {r.path or 'غير مرفق'} — {'متاح دون اتصال' if r.offline_ready else 'غير مرفق'}")
        if not rows:self.list.addItem("لا توجد وسائط لهذا المستوى بعد.")
    def add_media(self):
        path,_=QFileDialog.getOpenFileName(self,"اختيار ملف","","وسائط (*.mp3 *.wav *.ogg *.mp4 *.m4a *.webm)")
        if not path:return
        source=Path(path); target=MEDIA_DIR/source.name; MEDIA_DIR.mkdir(parents=True,exist_ok=True)
        try:
            if source.resolve()!=target.resolve(): target.write_bytes(source.read_bytes())
            with SessionLocal() as s:
                s.add(MediaAsset(language=self.lang.currentText(),level=self.level.value(),kind=self.kind.currentText(),title=source.stem,path=str(target.relative_to(MEDIA_DIR)),source="local-import",offline_ready=True)); s.commit()
            self.refresh()
        except Exception as e: QMessageBox.critical(self,"فشل",str(e))
