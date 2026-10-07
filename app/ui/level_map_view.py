from PySide6.QtWidgets import QWidget,QVBoxLayout,QComboBox,QListWidget
from app.services import get_child
from app.learning import level_status

class LevelMapView(QWidget):
    def __init__(self):
        super().__init__(); layout=QVBoxLayout(self); self.language=QComboBox(); self.language.addItems(['ar','en']); layout.addWidget(self.language); self.list=QListWidget(); layout.addWidget(self.list); self.language.currentTextChanged.connect(self.refresh); self.refresh()
    def refresh(self):
        child=get_child(); self.list.clear()
        if not child:return
        for x in level_status(child.id,self.language.currentText()):
            state='✓ متقن' if x['mastered'] else ('جارٍ' if x['score'] else 'لم يبدأ')
            self.list.addItem(f"المستوى {x['level']} — {x['title']} — {x['score']:.0f}% — {state}")
