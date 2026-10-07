import json
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QPushButton,QRadioButton,QButtonGroup,QMessageBox,QProgressBar
from app.assessment import load_questions,options,grade,finish
from app.services import get_child

class QuestionBankView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); self.questions=[]; self.index=0; self.score=0
        filters=QHBoxLayout(); self.lang=QComboBox(); self.lang.addItems(["ar","en"]); self.level=QComboBox(); self.level.addItem("كل المستويات",-1)
        for i in range(13): self.level.addItem(str(i),i)
        self.skill=QComboBox(); self.skill.addItems(["كل المهارات","listening","speaking","reading","writing","vocabulary","grammar"])
        filters.addWidget(self.lang); filters.addWidget(self.level); filters.addWidget(self.skill); self.layout().addLayout(filters)
        self.start=QPushButton("بدء اختبار من بنك الأسئلة"); self.start.clicked.connect(self.begin); self.layout().addWidget(self.start)
        self.progress=QProgressBar(); self.layout().addWidget(self.progress)
        self.prompt=QLabel(); self.prompt.setWordWrap(True); self.layout().addWidget(self.prompt)
        self.group=QButtonGroup(self); self.options_buttons=[]; self.next=QPushButton("تأكيد الإجابة"); self.next.clicked.connect(self.answer); self.layout().addWidget(self.next)
        self.result=QLabel(); self.layout().addWidget(self.result)
    def begin(self):
        lv=self.level.currentData(); skill=self.skill.currentText()
        self.questions=load_questions(self.lang.currentText(),None if lv==-1 else lv,None if skill=="كل المهارات" else skill,10)
        self.index=0; self.score=0; self.result.clear()
        if not self.questions: QMessageBox.information(self,"تنبيه","لا توجد أسئلة لهذا الاختيار."); return
        self.progress.setMaximum(len(self.questions)); self.show_question()
    def show_question(self):
        for b in self.options_buttons: self.group.removeButton(b); b.deleteLater()
        self.options_buttons=[]
        if self.index>=len(self.questions): return
        q=self.questions[self.index]; self.prompt.setText(f"السؤال {self.index+1} من {len(self.questions)}: {q.prompt}")
        for option in options(q):
            b=QRadioButton(option); self.group.addButton(b); self.layout().insertWidget(self.layout().count()-2,b); self.options_buttons.append(b)
        self.progress.setValue(self.index)
    def answer(self):
        if self.index>=len(self.questions): return
        chosen=next((b.text() for b in self.options_buttons if b.isChecked()),None)
        if chosen is None: QMessageBox.information(self,"تنبيه","اختر إجابة أولاً."); return
        q=self.questions[self.index]
        if grade(q,chosen): self.score+=1
        self.index+=1
        if self.index<len(self.questions): self.show_question(); return
        child=get_child()
        r=finish(child.id,self.lang.currentText(),q.skill,q.level,len(self.questions),self.score) if child else None
        if r: self.result.setText(f"انتهى الاختبار — {r.correct}/{r.total} — النتيجة {r.score}%")
        self.prompt.setText("اكتمل الاختبار"); self.next.setEnabled(False)
