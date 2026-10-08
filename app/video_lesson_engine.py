"""سيناريوهات الفيديو التعليمية التفاعلية.
الملف لا يزعم أن الوسائط موجودة؛ يصف بدقة ما يجب أن يحتويه الفيلم الحقيقي.
"""
from dataclasses import dataclass,asdict
import json
@dataclass
class Scene:
    order:int; kind:str; character:str; dialogue:str; caption:str=""; action:str=""; interaction:dict|None=None; media_key:str=""
def build_video_script(language,age_group,level,title,skill,body):
    primary="ليان" if language=="ar" else "Lian"
    helper="سامي" if language=="ar" else "Sami"
    hello="مرحبًا يا بطل! اليوم سنتعلم شيئًا جديدًا." if language=="ar" else "Hello, champion! Today we will learn something new."
    prompt="كرر معي بصوت واضح، ثم اضغط «سمعتُها» عندما تنتهي." if language=="ar" else "Repeat after me clearly, then press “I said it” when you finish."
    check="ما الذي تعلمناه الآن؟ اختر الإجابة الصحيحة." if language=="ar" else "What did we learn? Choose the correct answer."
    scenes=[
      Scene(1,"intro",primary,hello,hello,"ظهور الشخصية وحركة ترحيب",media_key="intro"),
      Scene(2,"teach",primary,body,body,"شرح بصري مع تكبير الكلمة/الحرف",media_key="teach"),
      Scene(3,"dialogue",helper,prompt,prompt,"سامي يطلب من الطفل التقليد",media_key="repeat"),
      Scene(4,"pronunciation",primary,"الآن استمع للنطق ثم كرره.","Listen, then repeat.","إيقاف تلقائي وانتظار التسجيل",{"kind":"repeat","prompt":prompt}, "pronunciation"),
      Scene(5,"quiz",helper,check,check,"تظهر الخيارات وينتظر اختيار الطفل",{"kind":"choice","prompt":check}, "quiz"),
      Scene(6,"feedback",primary,"أحسنت! لنكررها مرة أخرى معًا.","Great! Let's repeat it together.","نجاح: احتفال؛ خطأ: تلميح ثم إعادة المشهد",media_key="feedback"),
      Scene(7,"outro",primary,"أراك في الدرس القادم!","See you in the next lesson!","إظهار النجمة والتقدم",media_key="outro"),
    ]
    return {"version":1,"language":language,"age_group":age_group,"level":level,"title":title,"skill":skill,"characters":[primary,helper],"scenes":[asdict(x) for x in scenes],"requirements":{"human_voice":True,"animated_characters":True,"captions":True,"interactive_pause":True,"pronunciation_activity":True}}
def serialize_script(script): return json.dumps(script,ensure_ascii=False)
