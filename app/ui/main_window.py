from PySide6.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QStackedWidget,QListWidget
from PySide6.QtCore import Qt
from app.services import get_child,dashboard
from app.ui.lesson_view import LessonView
from app.ui.words_view import WordsView
from app.ui.test_view import TestView
from app.ui.plan_view import PlanView
from app.ui.review_view import ReviewView
from app.ui.child_view import ChildView
from app.ui.games_view import GamesView
from app.ui.story_view import StoryView
from app.ui.speaking_view import SpeakingView
from app.ui.parent_view import ParentView
from app.ui.media_view import MediaView
from app.ui.assessment_view import AssessmentView
from app.ui.progress_view import ProgressView
from app.ui.dictionary_view import DictionaryView
from app.ui.settings_view import SettingsView
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("لغتي — مدرسة اللغات"); self.setLayoutDirection(Qt.RightToLeft)
        root=QWidget(); self.setCentralWidget(root); outer=QHBoxLayout(root); nav=QListWidget(); nav.setFixedWidth(220)
        nav.addItems(["الرئيسية","خطة اليوم","العربية","English","الكلمات","قاموس وبحث","المراجعة الذكية","الألعاب","القصص","التحدث والنطق","الاختبارات","تحديد المستوى","التقدم","ملف الطفل","ولي الأمر","الوسائط","الإعدادات"])
        self.stack=QStackedWidget(); outer.addWidget(nav); outer.addWidget(self.stack)
        widgets=[self.home(),PlanView(),LessonView("ar"),LessonView("en"),WordsView(),DictionaryView(),ReviewView(),GamesView(),StoryView(),SpeakingView(),TestView(),AssessmentView(),ProgressView(),ChildView(),ParentView(),MediaView(),SettingsView()]
        for w in widgets:self.stack.addWidget(w)
        nav.currentRowChanged.connect(self.stack.setCurrentIndex); nav.setCurrentRow(0)
    def home(self):
        w=QWidget(); l=QVBoxLayout(w); c=get_child(); done,mastered,avg=dashboard(c.id) if c else (0,0,0); t=QLabel("مرحبًا بك في لغتي"); t.setStyleSheet("font-size:30px;font-weight:bold;padding:20px"); l.addWidget(t); l.addWidget(QLabel(f"الدروس المنجزة: {done} | المتقنة: {mastered} | متوسط الاختبارات: {avg}%")); l.addWidget(QLabel("خطة التعلم • مراجعة ذكية • ألعاب • قصص • تحدث • اختبارات • تقدم • ولي الأمر")); l.addStretch(); return w
