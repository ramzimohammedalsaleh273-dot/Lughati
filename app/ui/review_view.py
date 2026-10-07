from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QHBoxLayout
from app.services import get_child
from app.review import due,schedule

class ReviewView(QWidget):
    def __init__(self):
        super().__init__(); self.child=get_child(); self.items=due(self.child.id) if self.child else []; self.index=0
        layout=QVBoxLayout(self); layout.addWidget(QLabel("المراجعة الذكية — التكرار المتباعد"))
        self.word=QLabel(); self.word.setStyleSheet("font-size:34px;padding:24px"); layout.addWidget(self.word)
        self.meaning=QLabel(); layout.addWidget(self.meaning)
        row=QHBoxLayout()
        for quality,title in [(1,"نسيت"),(3,"أتذكر"),(5,"أتقنت")]:
            b=QPushButton(title); b.clicked.connect(lambda _,q=quality:self.answer(q)); row.addWidget(b)
        layout.addLayout(row); self.show_item()
    def show_item(self):
        if self.index>=len(self.items): self.word.setText("انتهت المراجعة الحالية."); self.meaning.setText("لا توجد كلمات مستحقة الآن."); return
        _,word=self.items[self.index]; self.word.setText(word.text); self.meaning.setText("المعنى: "+word.meaning+"\nمثال: "+word.example)
    def answer(self,quality):
        if self.index<len(self.items):
            item,_=self.items[self.index]; schedule(self.child.id,item.word_id,quality); self.index+=1; self.show_item()
