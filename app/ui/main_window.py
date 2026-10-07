from PySide6.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QStackedWidget,QListWidget,QComboBox
from PySide6.QtCore import Qt
from app.services import get_child,children
from app.state import set_child,subscribe
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
from app.ui.skills_view import SkillsView
from app.ui.dashboard_view import DashboardView
from app.ui.question_bank_view import QuestionBankView
from app.ui.media_player_view import MediaPlayerView
from app.ui.children_manager_view import ChildrenManagerView
from app.ui.curriculum_view import CurriculumView
from app.ui.stories_library_view import StoriesLibraryView
from app.ui.daily_plan_view import DailyPlanView
from app.ui.achievements_view import AchievementsView
from app.ui.level_map_view import LevelMapView
from app.ui.help_view import HelpView
from app.ui.assistant_view import AssistantView
from app.ui.story_session_view import StorySessionView
from app.ui.practice_view import PracticeView
from app.ui.listening_view import ListeningView
from app.ui.mastery_view import MasteryView
from app.ui.recordings_view import RecordingsView
from app.ui.rich_assessment_view import RichAssessmentView
from app.ui.skill_dashboard_view import SkillDashboardView
from app.ui.diagnostics_view import DiagnosticsView
from app.ui.sync_view import SyncView
from app.ui.parent_report_view import ParentReportView
from app.ui.adventure_view import AdventureView
from app.ui.pronunciation_view import PronunciationView

class MainWindow(QMainWindow):
 def __init__(self):
  super().__init__(); self.setWindowTitle("لغتي — مدرسة اللغات"); self.setLayoutDirection(Qt.RightToLeft)
  root=QWidget(); self.setCentralWidget(root); outer=QHBoxLayout(root)
  side=QVBoxLayout(); self.child_box=QComboBox(); side.addWidget(QLabel("الطفل الحالي")); side.addWidget(self.child_box)
  nav=QListWidget(); nav.addItems(["الرئيسية","خطة اليوم","الخطة الذكية","العربية","English","المنهج","الكلمات","قاموس وبحث","المراجعة الذكية","الألعاب","القصص","مكتبة القصص","جلسة القصة","التحدث والنطق","مختبر تحليل النطق","التسجيلات","المغامرة التعليمية","الاستماع","بنك الأسئلة","الاختبارات","التقييم الشامل","تحديد المستوى","التقدم","خريطة المستويات","خريطة الإتقان","المهارات","لوحة المهارات","الإنجازات","ملف الطفل","الأطفال","ولي الأمر","تقرير ولي الأمر","الوسائط","مشغل الوسائط","تدريب الكتابة","المساعد","التشخيص","المزامنة","الإعدادات"]); side.addWidget(nav,1)
  self.stack=QStackedWidget(); outer.addLayout(side); outer.addWidget(self.stack,1); self.ui_errors=[]
  self.widgets=[DashboardView(),PlanView(),DailyPlanView(),LessonView("ar"),LessonView("en"),CurriculumView(),WordsView(),DictionaryView(),ReviewView(),GamesView(),StoryView(),StoriesLibraryView(),StorySessionView(),SpeakingView(),PronunciationView(),RecordingsView(),AdventureView(),ListeningView(),QuestionBankView(),TestView(),RichAssessmentView(),AssessmentView(),ProgressView(),LevelMapView(),MasteryView(),SkillsView(),SkillDashboardView(),AchievementsView(),ChildView(),ChildrenManagerView(),ParentView(),ParentReportView(),MediaView(),MediaPlayerView(),PracticeView(),AssistantView(),DiagnosticsView(),SyncView(),SettingsView()]
  for w in self.widgets:self.stack.addWidget(w)
  nav.currentRowChanged.connect(self.stack.setCurrentIndex); nav.setCurrentRow(0)
  self.child_box.currentIndexChanged.connect(self._select_child)
  subscribe(self.refresh_child_state); self.refresh_child_state()
 def refresh_child_state(self):
  current=get_child(); self.child_box.blockSignals(True); self.child_box.clear()
  data=children()
  for c in data:self.child_box.addItem(f"{c.name} — {c.age} سنة",c.id)
  if current:
   idx=self.child_box.findData(current.id)
   if idx>=0:self.child_box.setCurrentIndex(idx)
  self.child_box.blockSignals(False)
  for w in self.widgets:
   if hasattr(w,"refresh"):
    try:w.refresh()
    except Exception as exc:self.ui_errors.append(f"{type(w).__name__}: {exc}")
 def _select_child(self,index):
  cid=self.child_box.itemData(index)
  if cid is not None:set_child(cid)
 def closeEvent(self,event):
  try:
   from app.state import unsubscribe
   unsubscribe(self.refresh_child_state)
  except Exception:pass
  super().closeEvent(event)
