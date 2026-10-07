from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QLineEdit,QPushButton,QMessageBox
from app.sync_manager import sync_now,retry_failed,queue_count
from app.settings_service import get,set

class SyncView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("المزامنة الاختيارية عبر الإنترنت"))
        self.info=QLabel(); l.addWidget(self.info); self.endpoint=QLineEdit(get("sync_endpoint","")); self.endpoint.setPlaceholderText("رابط خادم المزامنة — اختياري"); l.addWidget(self.endpoint)
        b=QPushButton("إرسال المعلّق عند الاتصال"); b.clicked.connect(self.send); l.addWidget(b)
        b=QPushButton("إعادة محاولة الأحداث الفاشلة"); b.clicked.connect(self.retry); l.addWidget(b); self.refresh()
    def refresh(self): self.info.setText("الحالة: "+str(queue_count()))
    def send(self):
        try:
            set("sync_endpoint",self.endpoint.text().strip()); result=sync_now(self.endpoint.text().strip(),get("sync_token","")); self.info.setText(str(result)); self.refresh()
        except Exception as e: QMessageBox.warning(self,"المزامنة",str(e))
    def retry(self):
        n=retry_failed(); self.info.setText(f"تمت إعادة {n} أحداث إلى قائمة الانتظار."); self.refresh()
