from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QPushButton,QRadioButton,QButtonGroup,QLineEdit,QMessageBox
from app.services import words,get_child,save_test
from app.game_engine import MODES,round_for,check

class GamesView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("مختبر الألعاب التعليمية"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.mode=QComboBox(); self.mode.addItems(["المعنى","الكلمة من المعنى","الإملاء","بناء الكلمة","صح أم خطأ","المطابقة","الذاكرة","الجملة"]); l.addWidget(self.mode)
        self.start=QPushButton("جولة جديدة"); self.start.clicked.connect(self.new_round); l.addWidget(self.start)
        self.prompt=QLabel(); self.prompt.setWordWrap(True); l.addWidget(self.prompt)
        self.group=QButtonGroup(self); self.buttons=[]
        for _ in range(3):
            b=QRadioButton(); self.group.addButton(b); self.buttons.append(b); l.addWidget(b)
        self.text=QLineEdit(); self.text.setPlaceholderText("اكتب الإجابة"); l.addWidget(self.text)
        self.answer=QPushButton("تحقق"); self.answer.clicked.connect(self.grade); l.addWidget(self.answer)
        self.score_label=QLabel("النتيجة: 0/0"); l.addWidget(self.score_label)
        self.current=None; self.score=0; self.total=0
    def new_round(self):
        data=words(self.lang.currentText())
        mode=MODES[self.mode.currentIndex()]
        self.current=round_for(mode,data)
        if not self.current:QMessageBox.information(self,"تنبيه","لا توجد مفردات كافية.");return
        self.prompt.setText(self.current.prompt); self.text.clear()
        is_text=not self.current.choices
        self.text.setVisible(is_text)
        for i,b in enumerate(self.buttons):
            visible=i<len(self.current.choices); b.setVisible(visible); b.setText(self.current.choices[i] if visible else ""); b.setChecked(False)
    def grade(self):
        if not self.current:return
        chosen=self.text.text() if self.text.isVisible() else next((b.text() for b in self.buttons if b.isChecked()),"")
        if not chosen:QMessageBox.information(self,"تنبيه","اختر أو اكتب الإجابة.");return
        self.total+=1; self.score+=int(check(self.current,chosen)); self.score_label.setText(f"النتيجة: {self.score}/{self.total}")
        c=get_child()
        if c: save_test(c.id,self.lang.currentText(),"vocabulary",self.score/self.total*100)
        self.new_round()
