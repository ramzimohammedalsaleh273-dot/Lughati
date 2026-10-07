from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QComboBox,QTextEdit,QSpinBox
from app.services import get_child,lessons
from app.activity_engine import activities,finish_lesson

class LessonView(QWidget):
    def __init__(self,language):
        super().__init__(); self.language=language; self.data=lessons(language); l=QVBoxLayout(self)
        l.addWidget(QLabel("دروس اللغة العربية" if language=="ar" else "دروس اللغة الإنجليزية"))
        self.box=QComboBox(); self.box.addItems([f"المستوى {x.level}: {x.title}" for x in self.data]); l.addWidget(self.box)
        self.body=QTextEdit(); self.body.setReadOnly(True); l.addWidget(self.body)
        self.activity=QLabel(); l.addWidget(self.activity)
        self.score=QSpinBox(); self.score.setRange(0,100); self.score.setValue(100); self.score.setPrefix("درجة النشاط: "); l.addWidget(self.score)
        b=QPushButton("تسجيل إتمام الدرس"); b.clicked.connect(self.complete); l.addWidget(b); self.box.currentIndexChanged.connect(self.show_lesson); self.show_lesson(0)
    def show_lesson(self,i):
        if not self.data:return
        x=self.data[i]; self.body.setPlainText(x.body+"\n\nنفذ النشاط ثم قيّم أداءك بصدق.")
        acts=activities(x.id); self.activity.setText(f"عدد الأنشطة: {len(acts)} | "+("؛ ".join(a.kind for a in acts[:6]) if acts else "لا توجد أنشطة"))
    def complete(self):
        if self.data:
            c=get_child()
            if c:finish_lesson(c.id,self.data[self.box.currentIndex()].id,self.score.value()); self.body.append("\n✓ تم حفظ النتيجة وتحديث الإتقان.")
