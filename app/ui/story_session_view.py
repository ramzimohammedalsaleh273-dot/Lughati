from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QTextEdit,QLineEdit,QMessageBox
from app.services import stories
from app.story_engine import build_session,comprehension_score

class StorySessionView(QWidget):
    def __init__(self):
        super().__init__(); self.setLayout(QVBoxLayout()); l=self.layout()
        self.title=QLabel("جلسة قصة تفاعلية"); l.addWidget(self.title)
        self.body=QTextEdit(); self.body.setReadOnly(True); l.addWidget(self.body)
        self.question=QLabel(); l.addWidget(self.question)
        self.answer=QLineEdit(); l.addWidget(self.answer)
        self.check=QPushButton("تحقق من الفهم"); self.check.clicked.connect(self.grade); l.addWidget(self.check)
        self.result=QLabel(); l.addWidget(self.result); self.data=[]; self.session=None; self.index=0
        self.start()
    def start(self):
        self.data=stories("ar")
        if self.data:self.session=build_session(self.data[0]); self.body.setPlainText(self.session.body); self.next_question()
    def next_question(self):
        if self.session and self.index<len(self.session.questions):
            q=self.session.questions[self.index]; self.question.setText(q.get("prompt","")); self.answer.clear()
        elif self.session:self.question.setText("انتهت أسئلة القصة.")
    def grade(self):
        if not self.session or self.index>=len(self.session.questions):return
        q=self.session.questions[self.index]; ok=self.answer.text().strip().casefold()==str(q.get("answer","")).strip().casefold()
        self.result.setText("إجابة صحيحة" if ok else "حاول مرة أخرى")
        if ok:self.index+=1; self.next_question()
