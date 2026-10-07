from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton
from app.sync import status,push

class SyncView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("المزامنة الاختيارية عبر الإنترنت")); self.info=QLabel(); l.addWidget(self.info)
        self.endpoint=QLineEdit(); self.endpoint.setPlaceholderText("رابط خادم المزامنة — اختياري"); l.addWidget(self.endpoint)
        b=QPushButton("إرسال المعلّق عند الاتصال"); b.clicked.connect(self.send); l.addWidget(b); self.refresh()
    def refresh(self): self.info.setText(str(status()))
    def send(self):
        url=self.endpoint.text().strip()
        self.info.setText(str(push(url)) if url else "أدخل رابط الخادم أولاً")
