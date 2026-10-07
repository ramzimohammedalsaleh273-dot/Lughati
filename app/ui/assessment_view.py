from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QRadioButton,QButtonGroup
from app.services import get_child,save_test
class AssessmentView(QWidget):
    def __init__(self):
        super().__init__(); self.questions=[("أي مهارة تعني فهم الكلام المسموع؟",["الاستماع","الكتابة","الرسم"],0),("أي كلمة تعني كتابًا؟",["book","water","sun"],0),("ما أول خطوة مناسبة للمبتدئ؟",["تعلم الأصوات والحروف","قراءة نص طويل","دراسة النحو المتقدم"],0)]; self.i=0; self.score=0; l=QVBoxLayout(self); l.addWidget(QLabel("تقييم تحديد المستوى")); self.q=QLabel(); l.addWidget(self.q); self.g=QButtonGroup(self); self.r=[]
        for i in range(3): r=QRadioButton(); self.g.addButton(r,i); self.r.append(r); l.addWidget(r)
        self.b=QPushButton("التالي"); self.b.clicked.connect(self.next); l.addWidget(self.b); self.out=QLabel(); l.addWidget(self.out); self.showq()
    def showq(self):
        if self.i<len(self.questions):
            q,o,_=self.questions[self.i]; self.q.setText(q)
            for r,t in zip(self.r,o): r.setText(t); r.setChecked(False)
    def next(self):
        if self.i>=len(self.questions): return
        self.score+=self.g.checkedId()==self.questions[self.i][2]; self.i+=1
        if self.i<len(self.questions): self.showq()
        else:
            pct=self.score/len(self.questions)*100; save_test(get_child().id,"mixed","placement",pct); self.q.setText("اكتمل التقييم"); self.out.setText(f"نتيجتك: {pct:.0f}% — ستُستخدم كبداية أولية لخطة التعلم."); self.b.setEnabled(False)
