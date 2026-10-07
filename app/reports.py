from datetime import datetime
from pathlib import Path
import csv
from app.database import SessionLocal
from app.models import Child,Progress,TestResult,Lesson

def export_child_report(child_id,path):
    with SessionLocal() as s:
        child=s.get(Child,child_id)
        rows=s.query(Progress,Lesson).join(Lesson,Progress.lesson_id==Lesson.id).filter(Progress.child_id==child_id).all()
        tests=s.query(TestResult).filter(TestResult.child_id==child_id).all()
    p=Path(path)
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f); w.writerow(['تقرير لغتي']); w.writerow(['الطفل',child.name if child else '']); w.writerow(['تاريخ التقرير',datetime.now().isoformat(timespec='seconds')]); w.writerow([]); w.writerow(['اللغة','المستوى','الدرس','الدرجة','متقن'])
        for prog,lesson in rows:w.writerow([lesson.language,lesson.level,lesson.title,prog.score,'نعم' if prog.mastered else 'لا'])
        w.writerow([]); w.writerow(['اللغة','المهارة','الدرجة'])
        for t in tests:w.writerow([t.language,t.skill,t.score])
    return p
