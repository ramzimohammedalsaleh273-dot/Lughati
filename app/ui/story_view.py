from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QTextEdit,QPushButton
class StoryView(QWidget):
    def __init__(self):
        super().__init__(); l=QVBoxLayout(self); l.addWidget(QLabel("قصص لغتي")); self.text=QTextEdit(); self.text.setReadOnly(True); self.text.setPlainText("قصة: يوم جميل\n\nاستيقظ سامي مبكرًا. فتح النافذة ورأى الشمس. غسل يديه، ثم جلس مع أسرته وتناول فطوره. بعد ذلك أخذ كتابه وبدأ يقرأ.\n\nسؤال الفهم: ماذا أخذ سامي؟"); l.addWidget(self.text); b=QPushButton("قرأت القصة وفهمتها"); b.clicked.connect(lambda:self.text.append("\n✓ سُجلت القراءة.")); l.addWidget(b)
