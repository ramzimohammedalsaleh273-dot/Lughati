from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QLineEdit,QComboBox
import random

class GamesView(QWidget):
    def __init__(self):
        super().__init__(); self.items=[("أب","father"),("بيت","house"),("قلم","pen"),("ماء","water"),("كتاب","book"),("شمس","sun")]; self.index=0; self.score=0
        layout=QVBoxLayout(self); layout.addWidget(QLabel("مختبر الألعاب التعليمية"))
        self.mode=QComboBox(); self.mode.addItems(["ترجمة الكلمات","اختيار الإجابة","تحدي سريع"]); layout.addWidget(self.mode)
        self.question=QLabel(); layout.addWidget(self.question); self.answer=QLineEdit(); self.answer.setPlaceholderText("اكتب الإجابة"); layout.addWidget(self.answer)
        self.button=QPushButton("تحقق"); self.button.clicked.connect(self.check); layout.addWidget(self.button); self.result=QLabel(); layout.addWidget(self.result)
        self.mode.currentIndexChanged.connect(self.show_question); self.show_question()
    def show_question(self):
        a,b=self.items[self.index]; self.answer.clear()
        if self.mode.currentIndex()==0: self.question.setText("ما ترجمة: "+a+"؟")
        elif self.mode.currentIndex()==1:
            choices=[b]+[x[1] for x in random.sample(self.items,2)]; random.shuffle(choices); self.question.setText("اختر ترجمة "+a+" من: "+" / ".join(choices))
        else: self.question.setText("تحدي سريع: اكتب معنى "+a)
    def check(self):
        a,b=self.items[self.index]; ok=self.answer.text().strip().lower()==b.lower(); self.result.setText("✓ إجابة صحيحة" if ok else "الإجابة الصحيحة: "+b); self.score+=int(ok); self.index=(self.index+1)%len(self.items); self.show_question()
