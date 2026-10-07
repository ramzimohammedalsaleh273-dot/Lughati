from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QListWidget
from app.config import MEDIA_DIR
class MediaView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("مكتبة الصوت والفيديو المحلية")); self.list=QListWidget(); l.addWidget(self.list); self.refresh()
    def refresh(self):
        self.list.clear(); files=sorted([p for p in MEDIA_DIR.rglob("*") if p.is_file()])
        self.list.addItems([str(p.relative_to(MEDIA_DIR)) for p in files] or ["لا توجد وسائط بعد — ضع ملفات مرخصة داخل مجلد media."])
