from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QCheckBox,QPushButton,QFileDialog,QMessageBox
from app.config import OFFLINE_FIRST,INTERNET_REQUIRED
from app.backup import backup_database,restore_database

class SettingsView(QWidget):
    def __init__(self):
        super().__init__(); layout=QVBoxLayout(self); layout.addWidget(QLabel("إعدادات لغتي"))
        offline=QCheckBox("الوضع دون اتصال — مفعل"); offline.setChecked(OFFLINE_FIRST); offline.setEnabled(False); layout.addWidget(offline)
        online=QCheckBox("الإنترنت مطلوب"); online.setChecked(INTERNET_REQUIRED); online.setEnabled(False); layout.addWidget(online)
        b=QPushButton("إنشاء نسخة احتياطية الآن"); b.clicked.connect(self.backup); layout.addWidget(b)
        r=QPushButton("استعادة نسخة احتياطية"); r.clicked.connect(self.restore); layout.addWidget(r)
        self.msg=QLabel(); layout.addWidget(self.msg)
    def backup(self): self.msg.setText("✓ "+str(backup_database()))
    def restore(self):
        path,_=QFileDialog.getOpenFileName(self,"اختيار النسخة الاحتياطية","","قاعدة البيانات (*.db)")
        if not path: return
        try:
            restore_database(path); QMessageBox.information(self,"تم","تمت الاستعادة. أغلق التطبيق وافتحه مجددًا.")
        except Exception as e: QMessageBox.critical(self,"فشل الاستعادة",str(e))
