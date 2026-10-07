from PySide6.QtWidgets import QApplication,QMessageBox
from app.database import init_db
from app.seed import seed_content
from app.validation import full_check
from app.ui.main_window import MainWindow

def create_app():
    app=QApplication([])
    app.setApplicationName("لغتي"); app.setOrganizationName("Lughati")
    app.setStyle("Fusion")
    init_db(); seed_content()
    check=full_check()
    if not check["ok"]:
        QMessageBox.critical(None,"فحص لغتي","تعذر بدء التطبيق لأن قاعدة البيانات أو المحتوى غير مكتمل.\n"+str(check))
        raise RuntimeError("فشل فحص جاهزية التطبيق")
    window=MainWindow(); window.showMaximized(); return app
