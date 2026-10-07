import json
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QPushButton,QRadioButton,QButtonGroup,QMessageBox
from sqlalchemy import select
from app.database import SessionLocal
from app.models import Child,Question
from app.services import save_test

class QuestionBankView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); self.questions=[]; self.index=0; self.score=0
        self.layout().addWidget(QLabel("بنك الاختبارات الشامل"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); self.layout().addWidget(self.lang)
        b=QPushButton("ابدأ الاختبار"); b.clicked.connect(self.begin); self.layout().addWidget(b)
        self.prompt=QLabel(); self.layout().addWidget(self.prompt)
        self.group=QButtonGroup(self); self.options=[]
        self.next=QPushButton("إجابة وانتقل"); self.next.clicked.connect(self.answer); self.layout().addWidget(self.next)
    def begin(self):
        with SessionLocal() as s: self.questions=list(s.scalars(select(Question).where(Question.language==self.lang.currentText()).order_by(Question.level,Question.id)).all())
        self.index=0; self.score=0; self.show_question()
    def show_question(self):
        for b in self.options: self.group.removeButton(b); b.deleteLater()
        self.options=[]
        if self.index>=len(self.questions): return
        q=self.questions[self.index]; self.prompt.setText(str(self.index+1)+". "+q.prompt)
        for option in json.loads(q.options):
            b=QRadioButton(option); self.group.addButton(b); self.layout().insertWidget(self.layout().count()-1,b); self.options.append(b)
    def answer(self):
        if self.index>=len(self.questions): return
        q=self.questions[self.index]; chosen=next((b.text() for b in self.options if b.isChecked()),None)
        if chosen is None: QMessageBox.information(self,"تنبيه","اختر إجابة أولاً."); return
        self.score += int(chosen==q.answer); self.index+=1
        if self.index>=len(self.questions):
            with SessionLocal() as s: child=s.scalar(select(Child).order_by(Child.id))
            if child: save_test(child.id,q.language,q.skill,round(self.score/len(self.questions)*100,1))
            QMessageBox.information(self,"النتيجة","نتيجتك: "+str(self.score)+"/"+str(len(self.questions))); self.prompt.setText("انتهى الاختبار"); return
        self.show_question()