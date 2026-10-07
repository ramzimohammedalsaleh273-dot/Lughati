from PySide6.QtWidgets import QWidget,QVBoxLayout,QLineEdit,QListWidget,QLabel
from app.services import words
class DictionaryView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("البحث الشامل في الكلمات")); self.search=QLineEdit(); self.search.setPlaceholderText("اكتب كلمة بالعربية أو الإنجليزية"); l.addWidget(self.search); self.list=QListWidget(); l.addWidget(self.list); self.data=words("ar")+words("en"); self.search.textChanged.connect(self.refresh); self.refresh("")
    def refresh(self,q):
        q=q.strip().lower(); self.list.clear();
        for w in self.data:
            if not q or q in w.text.lower() or q in w.meaning.lower(): self.list.addItem(f"{w.text} — {w.meaning} | {w.example}")
