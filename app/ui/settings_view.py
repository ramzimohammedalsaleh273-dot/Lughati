from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QCheckBox,QPushButton
from app.config import OFFLINE_FIRST,INTERNET_REQUIRED
from app.backup import backup_database
class SettingsView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("الإعدادات")); c=QCheckBox("الوضع دون اتصال — مفعل"); c.setChecked(OFFLINE_FIRST); c.setEnabled(False); l.addWidget(c); n=QCheckBox("الإنترنت مطلوب"); n.setChecked(INTERNET_REQUIRED); n.setEnabled(False); l.addWidget(n); b=QPushButton("إنشاء نسخة احتياطية الآن"); b.clicked.connect(self.backup); l.addWidget(b); self.msg=QLabel(); l.addWidget(self.msg)
    def backup(self): self.msg.setText("✓ تم إنشاء النسخة: "+str(backup_database()))
