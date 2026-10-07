import os
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
from PySide6.QtWidgets import QApplication
from app.database import init_db
from app.seed import seed_content

def test_main_window_constructs():
    init_db(); seed_content()
    app=QApplication.instance() or QApplication([])
    from app.ui.main_window import MainWindow
    window=MainWindow()
    assert window.stack.count() >= 30
    window.close()
