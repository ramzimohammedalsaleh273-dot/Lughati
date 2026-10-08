from pathlib import Path
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QListWidget,QPushButton,QFileDialog,QMessageBox,QComboBox,QSpinBox,QGroupBox
from app.config import MEDIA_DIR
from app.database import SessionLocal
from app.models import MediaAsset
from app.licensed_media import catalog as licensed_catalog, download_item
class MediaView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("مكتبة الصوت والفيديو المحلية والمرخّصة"))
        row=QHBoxLayout(); self.lang=QComboBox(); self.lang.addItems(["ar","en"]); self.level=QSpinBox(); self.level.setRange(0,12); self.kind=QComboBox(); self.kind.addItems(["audio","video"]); row.addWidget(self.lang); row.addWidget(self.level); row.addWidget(self.kind); l.addLayout(row)
        self.list=QListWidget(); l.addWidget(self.list,1)
        add=QPushButton("إضافة ملف وسائط مرخّص من الجهاز"); add.clicked.connect(self.add_media); l.addWidget(add)
        box=QGroupBox("فيديوهات تعليمية مرخّصة"); bl=QVBoxLayout(box); self.licensed=QListWidget(); bl.addWidget(self.licensed)
        br=QHBoxLayout(); self.download=QPushButton("تنزيل المحدد للعمل دون إنترنت"); self.open_source=QPushButton("فتح صفحة المصدر"); br.addWidget(self.download); br.addWidget(self.open_source); bl.addLayout(br); l.addWidget(box)
        self.download.clicked.connect(self.download_selected); self.open_source.clicked.connect(self.open_source_page); self.refresh()
    def refresh(self):
        self.list.clear()
        with SessionLocal() as s:
            rows=list(s.query(MediaAsset).filter_by(language=self.lang.currentText(),level=self.level.value(),kind=self.kind.currentText()).order_by(MediaAsset.id).all())
        for r in rows:self.list.addItem(f"{r.title} — {r.path or 'غير مرفق'} — {'متاح دون اتصال' if r.offline_ready else 'غير مرفق'}")
        if not rows:self.list.addItem("لا توجد وسائط لهذا المستوى بعد.")
        self.licensed.clear()
        for x in licensed_catalog():
            self.licensed.addItem(f"{'✓ محلي' if x['downloaded'] else 'تنزيل'} | {x['language']} | {x['title']} | {x['license']}")
            self.licensed.item(self.licensed.count()-1).setData(256,x["id"])
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
    def _selected_id(self):
        item=self.licensed.currentItem(); return item.data(256) if item else None
    def download_selected(self):
        item_id=self._selected_id()
        if not item_id:return
        try:
            path=download_item(item_id); meta=next(x for x in licensed_catalog() if x["id"]==item_id)
            with SessionLocal() as s:
                existing=s.query(MediaAsset).filter_by(language=meta["language"],level=meta["level"],kind="video",title=meta["title"]).first()
                if not existing:s.add(MediaAsset(language=meta["language"],level=meta["level"],kind="video",title=meta["title"],path=str(path),source=meta["source_page"],offline_ready=True))
                else: existing.path=str(path); existing.source=meta["source_page"]; existing.offline_ready=True
                s.commit()
            self.refresh(); QMessageBox.information(self,"تم","تم تنزيل الفيديو وحفظه محليًا. يمكن تشغيله دون اتصال.")
        except Exception as e: QMessageBox.critical(self,"فشل التنزيل",str(e))
    def open_source_page(self):
        item_id=self._selected_id()
        if not item_id:return
        import webbrowser; meta=next(x for x in licensed_catalog() if x["id"]==item_id); webbrowser.open(meta["source_page"])
