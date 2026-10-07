from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QCheckBox,QPushButton,QFileDialog,QMessageBox,QLineEdit,QFormLayout
from app.config import OFFLINE_FIRST,INTERNET_REQUIRED
from app.backup_manager import backup_database_safe,restore_database_safe
from app.content_exchange import export_content,import_content
from app.settings_service import get,set,ensure_defaults

class SettingsView(QWidget):
    def __init__(self):
        super().__init__(); ensure_defaults(); layout=QVBoxLayout(self); layout.addWidget(QLabel("إعدادات لغتي"))
        offline=QCheckBox("الوضع دون اتصال — مفعل"); offline.setChecked(OFFLINE_FIRST); offline.setEnabled(False); layout.addWidget(offline)
        online=QCheckBox("الإنترنت مطلوب"); online.setChecked(INTERNET_REQUIRED); online.setEnabled(False); layout.addWidget(online)
        form=QFormLayout(); self.minutes=QLineEdit(get("daily_minutes","20")); self.endpoint=QLineEdit(get("sync_endpoint","")); form.addRow("دقائق الخطة اليومية:",self.minutes); form.addRow("خادم المزامنة:",self.endpoint); layout.addLayout(form)
        b=QPushButton("حفظ الإعدادات"); b.clicked.connect(self.save); layout.addWidget(b)
        for title,fn in [("إنشاء نسخة احتياطية آمنة",self.backup),("استعادة نسخة احتياطية",self.restore),("تصدير حزمة المحتوى",self.export),("استيراد حزمة المحتوى",self.import_pack)]:
            b=QPushButton(title); b.clicked.connect(fn); layout.addWidget(b)
        self.msg=QLabel(); layout.addWidget(self.msg)
    def save(self):
        set("daily_minutes",self.minutes.text().strip()); set("sync_endpoint",self.endpoint.text().strip()); self.msg.setText("✓ تم حفظ الإعدادات")
    def backup(self):
        try:self.msg.setText("✓ "+str(backup_database_safe()))
        except Exception as e:self.msg.setText("✗ "+str(e))
    def restore(self):
        path,_=QFileDialog.getOpenFileName(self,"اختيار النسخة الاحتياطية","","قاعدة البيانات (*.db)")
        if not path:return
        try: result=restore_database_safe(path); QMessageBox.information(self,"تم","تمت الاستعادة، وتم إنشاء نسخة أمان قبلها."); self.msg.setText(str(result))
        except Exception as e:QMessageBox.critical(self,"فشل الاستعادة",str(e))
    def export(self):
        path,_=QFileDialog.getSaveFileName(self,"حفظ حزمة المحتوى","","حزمة لغتي (*.lughati)")
        if path:
            try:self.msg.setText("✓ "+str(export_content(path)))
            except Exception as e:self.msg.setText("✗ "+str(e))
    def import_pack(self):
        path,_=QFileDialog.getOpenFileName(self,"اختيار حزمة محتوى","","حزمة لغتي (*.lughati)")
        if not path:return
        try: QMessageBox.information(self,"تم","تم الاستيراد: "+str(import_content(path)))
        except Exception as e:QMessageBox.critical(self,"فشل الاستيراد",str(e))
