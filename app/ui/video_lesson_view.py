from pathlib import Path
import json
from PySide6.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QPushButton,QTextEdit,QMessageBox
from app.video_lesson_service import video_lessons
class VideoLessonView(QWidget):
    def __init__(self):
        super().__init__(); self.items=[]; l=QVBoxLayout(self)
        l.addWidget(QLabel("🎬 الدروس المرئية التفاعلية — ليان وسامي"))
        self.box=QComboBox(); l.addWidget(self.box)
        self.scene=QLabel(); l.addWidget(self.scene)
        self.dialogue=QTextEdit(); self.dialogue.setReadOnly(True); l.addWidget(self.dialogue,1)
        row=QHBoxLayout(); self.prev=QPushButton("المشهد السابق"); self.next=QPushButton("المشهد التالي"); self.repeat=QPushButton("كرر النطق"); row.addWidget(self.prev); row.addWidget(self.next); row.addWidget(self.repeat); l.addLayout(row)
        self.box.currentIndexChanged.connect(self.load); self.prev.clicked.connect(self.prev_scene); self.next.clicked.connect(self.next_scene); self.repeat.clicked.connect(self.repeat_scene); self.refresh()
    def refresh(self):
        self.items=video_lessons(); self.box.blockSignals(True); self.box.clear()
        for x in self.items:self.box.addItem(f"{x.language} | {x.age_group} | المستوى {x.level} | {x.title} | {x.status}",x.id)
        self.box.blockSignals(False)
        if self.items:self.load(0)
    def load(self,i):
        if not self.items:return
        self.index=0; self.current=self.items[i]; self.render()
    def render(self):
        data=json.loads(self.current.manifest); sc=data["scenes"][self.index]
        self.scene.setText(f"المشهد {sc['order']} — {sc['kind']} — الشخصية: {sc['character']}")
        self.dialogue.setPlainText(sc["dialogue"]+"\n\nالنص الظاهر: "+sc.get("caption","")+
            "\n\n"+("🎮 هذا المشهد ينتظر تفاعل الطفل." if sc.get("interaction") else ""))
    def next_scene(self):
        if hasattr(self,"current"):
            data=json.loads(self.current.manifest); self.index=min(self.index+1,len(data["scenes"])-1); self.render()
    def prev_scene(self):
        if hasattr(self,"current"):
            self.index=max(self.index-1,0); self.render()
    def repeat_scene(self):
        if hasattr(self,"current"): self.render()
