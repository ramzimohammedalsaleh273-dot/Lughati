import json
from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QComboBox,QPushButton,QRadioButton,QButtonGroup,QLineEdit,QTextEdit,QMessageBox
from app.services import get_child
from app.assessment import load_questions,finish
from app.assessment_engine import grade_item

class RichAssessmentView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("التقييم الشامل للمهارات"))
        self.lang=QComboBox(); self.lang.addItems(["ar","en"]); l.addWidget(self.lang)
        self.level=QComboBox(); self.level.addItems([str(x) for x in range(13)]); l.addWidget(self.level)
        self.start=QPushButton("بدء تقييم"); self.start.clicked.connect(self.begin); l.addWidget(self.start)
        self.prompt=QLabel(); self.prompt.setWordWrap(True); l.addWidget(self.prompt)
        self.group=QButtonGroup(self); self.radios=[]
        for _ in range(3):
            r=QRadioButton(); self.group.addButton(r); self.radios.append(r); l.addWidget(r)
        self.text=QLineEdit(); self.text.hide(); l.addWidget(self.text)
        self.next=QPushButton("التالي"); self.next.clicked.connect(self.advance); l.addWidget(self.next)
        self.out=QLabel(); l.addWidget(self.out); self.items=[]; self.i=0; self.correct=0
    def begin(self):
        self.items=load_questions(self.lang.currentText(),int(self.level.currentText()),limit=12); self.i=0; self.correct=0
        if not self.items: QMessageBox.information(self,"تنبيه","لا توجد أسئلة لهذا المستوى."); return
        self.next.setEnabled(True); self.show_item()
    def show_item(self):
        q=self.items[self.i]; self.prompt.setText(f"{self.i+1}/{len(self.items)} — {q.prompt}")
        vals=[]
        try:
            p=json.loads(q.options or "[]"); vals=p.get("options",[]) if isinstance(p,dict) else p
        except Exception: vals=[]
        for i,r in enumerate(self.radios): r.setText(str(vals[i]) if i<len(vals) else ""); r.setVisible(i<len(vals)); r.setChecked(False)
        needs_text=(not vals) or q.skill in ("writing","listening")
        self.text.setVisible(needs_text); self.text.clear()
    def advance(self):
        if not self.items:return
        q=self.items[self.i]
        vals=[r.text() for r in self.radios if r.isVisible()]
        answer=next((r.text() for r in self.radios if r.isVisible() and r.isChecked()),None) if vals else self.text.text()
        if answer is None or not str(answer).strip(): QMessageBox.information(self,"تنبيه","أدخل إجابة."); return
        self.correct+=int(grade_item(q,answer)); self.i+=1
        if self.i<len(self.items): self.show_item(); return
        c=get_child()
        if c:
            result=finish(c.id,self.lang.currentText(),"mixed",int(self.level.currentText()),len(self.items),self.correct)
            self.out.setText(f"النتيجة {result.score}% — المستوى المختبر {result.level}")
        self.next.setEnabled(False)
