from dataclasses import dataclass
import random

@dataclass
class Round:
    mode:str
    prompt:str
    choices:list[str]
    answer:str

def _pick(items,n=3):
    return random.sample(items,min(n,len(items)))

def round_for(mode, words):
    pool=list(words)
    if len(pool)<3: raise ValueError("تحتاج اللعبة إلى ثلاث كلمات على الأقل")
    item=random.choice(pool)
    others=[x for x in pool if x.id!=item.id]
    choices=[item.meaning]+[x.meaning for x in random.sample(others,min(2,len(others)))]
    random.shuffle(choices)
    if mode=="meaning": return Round(mode,f"ما معنى «{item.text}»؟",choices,item.meaning)
    if mode=="reverse": 
        choices=[item.text]+[x.text for x in random.sample(others,min(2,len(others)))]
        random.shuffle(choices)
        return Round(mode,f"اختر الكلمة التي تعني «{item.meaning}».",choices,item.text)
    if mode=="spelling":
        return Round(mode,f"اكتب الكلمة: {item.meaning}",[],item.text)
    if mode=="true_false":
        claim=random.choice(pool).meaning
        truth=(claim==item.meaning)
        return Round(mode,f"هل «{item.text}» تعني «{claim}»؟",["صحيح","خطأ"],"صحيح" if truth else "خطأ")
    return Round(mode,f"ما معنى «{item.text}»؟",choices,item.meaning)
