from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QRadioButton,QButtonGroup,QComboBox,QMessageBox
from app.assessment import load_questions,options,grade,finish
from app.services import get_child

class TestView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); l=self.layout()
        l.addWidget(QLabel("الاختبار السريع"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.start=QPushButton("بدء اختبار المستوى"); self.start.clicked.connect(self.begin); l.addWidget(self.start)
        self.q=QLabel(); self.q.setWordWrap(True); l.addWidget(self.q)
        self.group=QButtonGroup(self); self.opts=[] 
        for _ in range(3):
            r=QRadioButton(); self.group.addButton(r); self.opts.append(r); l.addWidget(r)
        self.next=QPushButton("التالي"); self.next.clicked.connect(self.advance); l.addWidget(self.next)
        self.result=QLabel(); l.addWidget(self.result)
    def begin(self):
        self.questions=load_questions(self.lang.currentText(),None,limit=5); self.i=0; self.score=0
        if not self.questions: QMessageBox.information(self,"تنبيه","لا توجد أسئلة."); return
        self.next.setEnabled(True); self.show_question()
    def show_question(self):
        q=self.questions[self.i]; self.q.setText(f"السؤال {self.i+1}/{len(self.questions)}: {q.prompt}")
        vals=options(q)
        for i,r in enumerate(self.opts):
            r.setText(vals[i] if i<len(vals) else ""); r.setVisible(i<len(vals)); r.setChecked(False)
    def advance(self):
        if not getattr(self,"questions",None): return
        q=self.questions[self.i]; chosen=next((r.text() for r in self.opts if r.isChecked()),None)
        if chosen is None: QMessageBox.information(self,"تنبيه","اختر إجابة."); return
        self.score += int(grade(q,chosen)); self.i+=1
        if self.i<len(self.questions): self.show_question(); return
        c=get_child()
        if c:
            r=finish(c.id,self.lang.currentText(),q.skill,q.level,len(self.questions),self.score)
            self.result.setText(f"النتيجة: {r.correct}/{r.total} — {r.score}%")
        self.q.setText("انتهى الاختبار"); self.next.setEnabled(False)
