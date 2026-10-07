"""تحليل نطق محلي قابل للعمل دون إنترنت."""
from difflib import SequenceMatcher
import re
def normalize(text): return re.sub(r"[^\w\u0600-\u06ff]+","",str(text).lower())
def score_pronunciation(target, recognized):
    t=normalize(target); r=normalize(recognized)
    if not t: return {"score":0.0,"level":"invalid","feedback":"لا يوجد نص هدف."}
    score=round(SequenceMatcher(None,t,r).ratio()*100,1)
    level="ممتاز" if score>=90 else "جيد جداً" if score>=75 else "يحتاج تدريباً" if score>=60 else "أعد المحاولة"
    return {"score":score,"level":level,"feedback":f"درجة المطابقة النصية {score}%. هذا تقييم تقريبي، وليس بديلاً عن نموذج نطق صوتي متخصص."}
def compare_attempts(target, attempts): return [score_pronunciation(target,a) for a in attempts]
