from PySide6.QtWidgets import QApplication
from app.database import init_db
from app.seed import seed_content
from app.ui.main_window import MainWindow

def create_app():
    app = QApplication([])
    app.setApplicationName("لغتي")
    app.setOrganizationName("Lughati")
    app.setStyle("Fusion")
    init_db()
    seed_content()
    window = MainWindow()
    window.showMaximized()
    return app
