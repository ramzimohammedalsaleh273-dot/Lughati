from dataclasses import dataclass
import random
@dataclass
class Round:
    mode:str
    prompt:str
    choices:list[str]
    answer:str
def round_for(mode,words):
    pool=list(words)
    if len(pool)<3:raise ValueError("تحتاج اللعبة إلى ثلاث كلمات على الأقل")
    item=random.choice(pool); others=[x for x in pool if x.id!=item.id]
    if mode=="meaning":
        choices=[item.meaning]+[x.meaning for x in random.sample(others,2)]; random.shuffle(choices); return Round(mode,f"ما معنى «{item.text}»؟",choices,item.meaning)
    if mode=="reverse":
        choices=[item.text]+[x.text for x in random.sample(others,2)]; random.shuffle(choices); return Round(mode,f"اختر الكلمة التي تعني «{item.meaning}».",choices,item.text)
    if mode=="spelling":return Round(mode,f"اكتب الكلمة: {item.meaning}",[],item.text)
    if mode=="build":
        chars=list(item.text.replace(" ","")); random.shuffle(chars); return Round(mode,f"رتب الحروف لتكوين كلمة: {' '.join(chars)}",[],item.text)
    claim=random.choice(pool).meaning; truth=claim==item.meaning
    return Round("true_false",f"هل «{item.text}» تعني «{claim}»؟",["صحيح","خطأ"],"صحيح" if truth else "خطأ")
