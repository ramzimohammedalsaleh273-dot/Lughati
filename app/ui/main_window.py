from PySide6.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QStackedWidget,QListWidget,QListWidgetItem
from PySide6.QtCore import Qt
from app.services import get_child,dashboard
from app.ui.lesson_view import LessonView
from app.ui.words_view import WordsView
from app.ui.test_view import TestView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("لغتي — مدرسة اللغات"); self.setLayoutDirection(Qt.RightToLeft)
        root=QWidget(); self.setCentralWidget(root); outer=QHBoxLayout(root)
        nav=QListWidget(); nav.setFixedWidth(190)
        for name in ["الرئيسية","الأكاديمية العربية","English Academy","الكلمات","الاختبارات"]: nav.addItem(QListWidgetItem(name))
        self.stack=QStackedWidget(); outer.addWidget(nav); outer.addWidget(self.stack)
        self.stack.addWidget(self.home()); self.stack.addWidget(LessonView("ar")); self.stack.addWidget(LessonView("en")); self.stack.addWidget(WordsView()); self.stack.addWidget(TestView())
        nav.currentRowChanged.connect(self.stack.setCurrentIndex); nav.setCurrentRow(0)
    def home(self):
        w=QWidget(); l=QVBoxLayout(w); child=get_child(); done,mastered,avg=dashboard(child.id) if child else (0,0,0)
        title=QLabel("مرحبًا بك في لغتي"); title.setStyleSheet("font-size:30px;font-weight:bold;padding:20px")
        l.addWidget(title); l.addWidget(QLabel(f"الدروس المنجزة: {done}    |    الدروس المتقنة: {mastered}    |    متوسط الاختبارات: {avg}%"))
        for t in ["خطة اليوم: درس قراءة + كلمات + اختبار قصير","المراجعة الذكية تتبع الأخطاء وتعيدها في الوقت المناسب","يعمل التطبيق محليًا دون الحاجة للإنترنت"]:
            l.addWidget(QLabel("• "+t))
        l.addStretch(); return w
