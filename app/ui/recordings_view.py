from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QListWidget,QPushButton,QMessageBox
from app.services import get_child
from app.recording import recordings

class RecordingsView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("سجل التحدث والتسجيلات"))
        self.list=QListWidget(); l.addWidget(self.list); b=QPushButton("تحديث"); b.clicked.connect(self.refresh); l.addWidget(b); self.refresh()
    def refresh(self):
        self.list.clear(); c=get_child()
        if not c:return
        for r in recordings(c.id): self.list.addItem(f"{r.language} — {r.prompt} — تقييم ذاتي {r.self_score}% — {r.path}")
