from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QRadioButton,QButtonGroup
from app.services import get_child,save_test
class TestView(QWidget):
    def __init__(self):
        super().__init__(); self.i=0; self.score=0; self.questions=[("ما معنى cat؟",["قطة","كتاب","ماء"],0),("ما معنى بيت؟",["house","sun","pen"],0),("اختر كلمة إنجليزية صحيحة للماء",["water","book","dog"],0)]
        l=QVBoxLayout(self); l.addWidget(QLabel("اختبار قصير")); self.q=QLabel(); l.addWidget(self.q); self.group=QButtonGroup(self); self.opts=[]
        for i in range(3):
            r=QRadioButton(); self.group.addButton(r,i); self.opts.append(r); l.addWidget(r)
        b=QPushButton("التالي"); b.clicked.connect(self.next); l.addWidget(b); self.showq()
    def showq(self):
        if self.i<len(self.questions):
            q,o,_=self.questions[self.i]; self.q.setText(q)
            for r,t in zip(self.opts,o): r.setText(t); r.setChecked(False)
    def next(self):
        if self.i>=len(self.questions): return
        if self.group.checkedId()==self.questions[self.i][2]: self.score+=1
        self.i+=1
        if self.i<len(self.questions): self.showq()
        else:
            pct=self.score/len(self.questions)*100; self.q.setText(f"انتهى الاختبار — نتيجتك {pct:.0f}%"); save_test(get_child().id,"mixed","vocabulary",pct)
            for r in self.opts: r.setEnabled(False)
