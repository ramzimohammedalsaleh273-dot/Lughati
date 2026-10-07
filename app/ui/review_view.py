from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QHBoxLayout
from app.services import get_child,words
from app.review import due,schedule
class ReviewView(QWidget):
    def __init__(self):
        super().__init__(); self.child=get_child(); self.items=due(self.child.id); self.i=0; l=QVBoxLayout(self); l.addWidget(QLabel("المراجعة الذكية")); self.word=QLabel(); self.word.setStyleSheet("font-size:32px;padding:30px"); l.addWidget(self.word); row=QHBoxLayout();
        for q,t in [(1,"نسيت"),(3,"أتذكر"),(5,"أتقنت")]:
            b=QPushButton(t); b.clicked.connect(lambda _,q=q:self.answer(q)); row.addWidget(b)
        l.addLayout(row); self.show_item()
    def show_item(self): self.word.setText("لا توجد عناصر مستحقة الآن." if self.i>=len(self.items) else f"الكلمة رقم {self.items[self.i].word_id}")
    def answer(self,q):
        if self.i<len(self.items): schedule(self.child.id,self.items[self.i].word_id,q); self.i+=1; self.show_item()
