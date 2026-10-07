import random
from dataclasses import dataclass

@dataclass
class GameRound:
    prompt: str
    answer: str
    choices: list[str]

def translation_round(words):
    if not words: return None
    w=random.choice(words)
    pool=[x.meaning for x in words if x.id!=w.id and x.meaning]
    choices=[w.meaning]+random.sample(pool,min(2,len(pool)))
    random.shuffle(choices)
    return GameRound(f"ما معنى «{w.text}»؟",w.meaning,choices)

def spelling_round(words):
    if not words: return None
    w=random.choice(words)
    letters=list(w.text); random.shuffle(letters)
    return GameRound("رتب الكلمة: "+" ".join(letters),w.text,[w.text])

def matching_round(words):
    if not words: return None
    w=random.choice(words)
    return GameRound(f"طابق الكلمة مع معناها: {w.text}",w.meaning,[w.meaning]+[x.meaning for x in random.sample(words,min(2,len(words)-1))])
