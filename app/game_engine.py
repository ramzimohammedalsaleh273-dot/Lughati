import random
from dataclasses import dataclass

@dataclass
class GameRound:
    mode:str
    prompt:str
    answer:str
    choices:list[str]
    payload:dict

MODES=("meaning","reverse","spelling","build","true_false","matching","memory","sentence")

def _sample(pool,item,n=2):
    others=[x for x in pool if x.id!=item.id and getattr(x,"meaning","")]
    return random.sample(others,min(n,len(others)))

def round_for(mode,words):
    pool=[x for x in words if getattr(x,"text","") and getattr(x,"meaning","")]
    if len(pool)<3: return None
    item=random.choice(pool)
    if mode=="meaning":
        choices=[item.meaning]+[x.meaning for x in _sample(pool,item)]
        random.shuffle(choices); return GameRound(mode,f"ما معنى «{item.text}»؟",item.meaning,choices,{"word":item.text})
    if mode=="reverse":
        choices=[item.text]+[x.text for x in _sample(pool,item)]
        random.shuffle(choices); return GameRound(mode,f"اختر الكلمة التي تعني «{item.meaning}».",item.text,choices,{"meaning":item.meaning})
    if mode=="spelling":
        return GameRound(mode,f"اكتب الكلمة التي معناها: {item.meaning}",item.text,[],{"meaning":item.meaning})
    if mode=="build":
        chars=list(item.text.replace(" ","")); random.shuffle(chars)
        return GameRound(mode,"رتب الحروف: "+" ".join(chars),item.text,[],{"letters":chars})
    if mode=="true_false":
        claim=random.choice(pool); truth=claim.id==item.id
        return GameRound(mode,f"هل «{item.text}» تعني «{claim.meaning}»؟","صحيح" if truth else "خطأ",["صحيح","خطأ"],{"truth":truth})
    if mode=="matching":
        choices=[item.meaning]+[x.meaning for x in _sample(pool,item)]
        random.shuffle(choices); return GameRound(mode,f"طابق «{item.text}» مع معناها.",item.meaning,choices,{"word":item.text})
    if mode=="memory":
        pair=random.choice(pool)
        return GameRound(mode,f"احفظ الكلمة ثم اختر معناها: «{pair.text}»",pair.meaning,[pair.meaning]+[x.meaning for x in _sample(pool,pair)],{"word":pair.text})
    sentence=item.example or f"{item.text}"
    return GameRound(mode,f"أكمل/استخدم الكلمة «{item.text}» في جملة.",item.text,[],{"example":sentence})

def check(round_obj,answer):
    return bool(round_obj) and str(answer or "").strip().casefold()==str(round_obj.answer).strip().casefold()
