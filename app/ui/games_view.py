from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QPushButton,QRadioButton,QButtonGroup,QMessageBox
from app.services import words,get_child,save_test
from app.game_engine import translation_round,matching_round

class GamesView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); l=self.layout()
        l.addWidget(QLabel("ألعاب التعلم"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.mode=QComboBox(); self.mode.addItems(["معنى الكلمة","مطابقة سريعة"]); l.addWidget(self.mode)
        self.start=QPushButton("ابدأ جولة"); self.start.clicked.connect(self.new_round); l.addWidget(self.start)
        self.prompt=QLabel(); self.prompt.setWordWrap(True); l.addWidget(self.prompt)
        self.group=QButtonGroup(self); self.buttons=[]
        for _ in range(3):
            b=QRadioButton(); self.group.addButton(b); self.buttons.append(b); l.addWidget(b)
        self.answer=QPushButton("تحقق"); self.answer.clicked.connect(self.check); l.addWidget(self.answer)
        self.score_label=QLabel("النتيجة: 0"); l.addWidget(self.score_label)
        self.words_data=[]; self.current=None; self.score=0; self.total=0
    def new_round(self):
        self.words_data=words(self.lang.currentText())
        if len(self.words_data)<3: QMessageBox.information(self,"تنبيه","أضف مفردات كافية."); return
        self.current=translation_round(self.words_data) if self.mode.currentIndex()==0 else matching_round(self.words_data)
        self.prompt.setText(self.current.prompt)
        for i,b in enumerate(self.buttons):
            b.setText(self.current.choices[i] if i<len(self.current.choices) else ""); b.setVisible(i<len(self.current.choices)); b.setChecked(False)
    def check(self):
        if not self.current: return
        chosen=next((b.text() for b in self.buttons if b.isChecked()),None)
        if chosen is None: QMessageBox.information(self,"تنبيه","اختر إجابة."); return
        self.total+=1; self.score+=int(chosen==self.current.answer); self.score_label.setText(f"النتيجة: {self.score}/{self.total}")
        self.new_round()
