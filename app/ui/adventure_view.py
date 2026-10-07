from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel,QListWidget,QPushButton
from app.adventure_engine import build_world,available_nodes,reward_for
from app.services import get_child
class AdventureView(QWidget):
    def __init__(self):
        super().__init__(); self.layout=QVBoxLayout(self)
        self.layout.addWidget(QLabel("مغامرة لغتي — افتح المهام بإتقان المهارات"))
        self.list=QListWidget(); self.layout.addWidget(self.list)
        self.btn=QPushButton("تحديث الخريطة"); self.btn.clicked.connect(self.refresh); self.layout.addWidget(self.btn)
        self.refresh()
    def refresh(self):
        self.list.clear(); lang="ar"
        for n in available_nodes(lang,[]):
            self.list.addItem(f"⭐ {n.title} | {n.skill} | +{n.reward} نقطة")
