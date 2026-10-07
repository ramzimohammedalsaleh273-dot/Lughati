from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QPushButton,QRadioButton,QButtonGroup,QLineEdit,QMessageBox
from app.services import words
from app.game_modes import round_for

class GamesView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("ألعاب التعلم"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.mode=QComboBox(); self.mode.addItems(["معنى الكلمة","الكلمة من المعنى","الإملاء","صح أم خطأ","بناء الكلمة"]); l.addWidget(self.mode)
        self.start=QPushButton("ابدأ جولة"); self.start.clicked.connect(self.new_round); l.addWidget(self.start)
        self.prompt=QLabel(); self.prompt.setWordWrap(True); l.addWidget(self.prompt)
        self.group=QButtonGroup(self); self.buttons=[]
        for _ in range(4):
            b=QRadioButton(); self.group.addButton(b); self.buttons.append(b); l.addWidget(b)
        self.text=QLineEdit(); self.text.setPlaceholderText("اكتب الإجابة"); self.text.hide(); l.addWidget(self.text)
        self.answer=QPushButton("تحقق"); self.answer.clicked.connect(self.check); l.addWidget(self.answer)
        self.score_label=QLabel("النتيجة: 0/0"); l.addWidget(self.score_label)
        self.current=None; self.score=0; self.total=0
    def new_round(self):
        data=words(self.lang.currentText())
        if len(data)<3:QMessageBox.information(self,"تنبيه","لا توجد مفردات كافية."); return
        mode=["meaning","reverse","spelling","true_false","build"][self.mode.currentIndex()]
        self.current=round_for(mode,data); self.prompt.setText(self.current.prompt); self.text.clear()
        is_text=mode in ("spelling","build"); self.text.setVisible(is_text)
        for i,b in enumerate(self.buttons):
            visible=not is_text and i<len(self.current.choices); b.setVisible(visible); b.setText(self.current.choices[i] if visible else ""); b.setChecked(False)
    def check(self):
        if not self.current:return
        chosen=self.text.text().strip() if self.text.isVisible() else next((b.text() for b in self.buttons if b.isChecked()),None)
        if not chosen:QMessageBox.information(self,"تنبيه","أدخل أو اختر إجابة."); return
        self.total+=1; self.score+=int(chosen.casefold()==self.current.answer.casefold()); self.score_label.setText(f"النتيجة: {self.score}/{self.total}"); self.new_round()
