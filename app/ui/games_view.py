from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QLineEdit
import random
class GamesView(QWidget):
    def __init__(self):
        super().__init__(); self.items=[("أب","father"),("بيت","house"),("قلم","pen"),("ماء","water")]; self.i=0; l=QVBoxLayout(self); l.addWidget(QLabel("ألعاب الكلمات")); self.q=QLabel(); l.addWidget(self.q); self.a=QLineEdit(); self.a.setPlaceholderText("اكتب الإجابة"); l.addWidget(self.a); b=QPushButton("تحقق ثم التالي"); b.clicked.connect(self.check); l.addWidget(b); self.result=QLabel(); l.addWidget(self.result); self.showq()
    def showq(self): self.q.setText(f"ما ترجمة: {self.items[self.i][0]}؟"); self.a.clear()
    def check(self):
        ok=self.a.text().strip().lower()==self.items[self.i][1]; self.result.setText("✓ ممتاز!" if ok else f"الإجابة الصحيحة: {self.items[self.i][1]}"); self.i=(self.i+1)%len(self.items); self.showq()
