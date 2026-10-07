from datetime import datetime
from pathlib import Path
import csv, json
from app.report_engine import child_summary

def export_child_report(child_id,path,fmt=None):
    path=Path(path)
    data=child_summary(child_id)
    fmt=(fmt or path.suffix.lstrip(".") or "csv").lower()
    path.parent.mkdir(parents=True,exist_ok=True)
    if fmt=="json":
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
        return path
    if fmt=="pdf":
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        doc=SimpleDocTemplate(str(path),pagesize=A4)
        styles=getSampleStyleSheet(); story=[]
        story.append(Paragraph("Lughati — تقرير تقدم الطفل",styles["Title"]))
        story.append(Paragraph(f"الطفل: {data['child']['name']} — العمر: {data['child']['age']}",styles["Normal"]))
        for lang,info in data["languages"].items():
            story.append(Spacer(1,8)); story.append(Paragraph(f"اللغة {lang}: الإكمال {info['completion']}% — الإتقان {info['mastery']}% — الاختبارات {info['tests']}",styles["Normal"]))
        story.append(Spacer(1,8)); story.append(Paragraph("إجمالي النشاط: "+json.dumps(data["totals"],ensure_ascii=False),styles["Normal"]))
        doc.build(story); return path
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["تقرير لغتي"]); w.writerow(["الطفل",data["child"]["name"]]); w.writerow(["العمر",data["child"]["age"]]); w.writerow(["تاريخ التقرير",datetime.now().isoformat(timespec="seconds")])
        for lang,info in data["languages"].items():
            w.writerow([]); w.writerow(["اللغة",lang]); w.writerow(["الإكمال %",info["completion"]]); w.writerow(["الإتقان %",info["mastery"]]); w.writerow(["الدروس",info["completed"]]); w.writerow(["الاختبارات",info["tests"]])
            w.writerow(["المهارة","الدرجة"])
            for skill,val in info["skills"].items(): w.writerow([skill,val])
        w.writerow([]); w.writerow(["الإجماليات"]); w.writerow(list(data["totals"].keys())); w.writerow(list(data["totals"].values()))
    return path
