from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QLineEdit,QPushButton
from app.services import get_child,save_test
from app.assessment import load_questions
class PracticeView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("تدريب الكتابة"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.start=QPushButton("ابدأ"); self.start.clicked.connect(self.begin); l.addWidget(self.start)
        self.prompt=QLabel(); l.addWidget(self.prompt); self.input=QLineEdit(); l.addWidget(self.input)
        self.check=QPushButton("تصحيح"); self.check.clicked.connect(self.grade); l.addWidget(self.check); self.result=QLabel(); l.addWidget(self.result)
    def begin(self):
        self.questions=load_questions(self.lang.currentText(),None,"writing",5); self.i=0; self.correct=0
        if self.questions: self.showq()
    def showq(self):
        self.prompt.setText(self.questions[self.i].prompt); self.input.clear()
    def grade(self):
        if not getattr(self,"questions",None): return
        self.correct+=int(self.input.text().strip().casefold()==self.questions[self.i].answer.strip().casefold()); self.i+=1
        if self.i<len(self.questions): self.showq()
        else:
            c=get_child()
            if c: save_test(c.id,self.lang.currentText(),"writing",self.correct/len(self.questions)*100)
            self.result.setText(f"النتيجة: {self.correct}/{len(self.questions)}")
