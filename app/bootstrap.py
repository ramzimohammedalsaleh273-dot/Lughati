from PySide6.QtWidgets import QApplication
from app.database import init_db
from app.seed import seed_content
from app.validation import full_check
from app.ui_qml import create_qml_app

def create_app():
    app=QApplication([])
    app.setApplicationName("لغتي")
    app.setOrganizationName("Lughati")
    app.setLayoutDirection(__import__("PySide6.QtCore",fromlist=["Qt"]).Qt.LayoutDirection.RightToLeft)
    init_db()
    seed_content()
    check=full_check()
    if not check["ok"]:
        raise RuntimeError("فشل فحص جاهزية التطبيق: " + str(check))
    return create_qml_app(app)
