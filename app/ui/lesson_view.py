from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QPushButton,QComboBox,QTextEdit
from app.services import get_child,lessons,save_lesson
class LessonView(QWidget):
    def __init__(self,language):
        super().__init__(); self.language=language; self.data=lessons(language); l=QVBoxLayout(self)
        l.addWidget(QLabel("دروس اللغة العربية" if language=="ar" else "دروس اللغة الإنجليزية"))
        self.box=QComboBox(); self.box.addItems([f"المستوى {x.level}: {x.title}" for x in self.data]); l.addWidget(self.box)
        self.body=QTextEdit(); self.body.setReadOnly(True); l.addWidget(self.body)
        b=QPushButton("إتمام الدرس — أتقنت"); b.clicked.connect(self.complete); l.addWidget(b); self.box.currentIndexChanged.connect(self.show_lesson); self.show_lesson(0)
    def show_lesson(self,i):
        if self.data: x=self.data[i]; self.body.setPlainText(x.body+"\n\nابدأ بالقراءة بصوت واضح، ثم أعد النشاط مرة أخرى.")
    def complete(self):
        if self.data: save_lesson(get_child().id,self.data[self.box.currentIndex()].id,100); self.body.append("\n✓ تم تسجيل الإتقان.")
