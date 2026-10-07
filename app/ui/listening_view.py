from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QPushButton,QLineEdit
from app.services import words,get_child,save_test
from app.tts import speak

class ListeningView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("مختبر الاستماع"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.word=QLabel(); l.addWidget(self.word)
        self.play=QPushButton("استمع"); self.play.clicked.connect(self.listen); l.addWidget(self.play)
        self.input=QLineEdit(); self.input.setPlaceholderText("اكتب ما سمعت"); l.addWidget(self.input)
        self.check=QPushButton("تحقق"); self.check.clicked.connect(self.grade); l.addWidget(self.check)
        self.result=QLabel(); l.addWidget(self.result); self.start()
    def start(self):
        self.data=words(self.lang.currentText()); self.i=0; self.correct=0
        if self.data: self.current=self.data[0]; self.word.setText("استمع ثم اكتب ما سمعت.")
    def listen(self):
        if getattr(self,"current",None): speak(self.current.text,self.lang.currentText())
    def grade(self):
        if not getattr(self,"current",None): return
        self.correct+=int(self.input.text().strip().casefold()==self.current.text.strip().casefold()); self.i+=1
        if self.i<len(self.data): self.current=self.data[self.i]; self.input.clear(); self.listen()
        else:
            c=get_child()
            if c: save_test(c.id,self.lang.currentText(),"listening",self.correct/len(self.data)*100)
            self.result.setText(f"النتيجة: {self.correct}/{len(self.data)}")