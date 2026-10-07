from app.database import SessionLocal
from app.models import Child, Lesson, Word

def seed_content():
    with SessionLocal() as s:
        if not s.query(Child).first(): s.add(Child(name="الطفل", age=6))
        if s.query(Lesson).count() == 0:
            lessons=[]
            arabic=[("الحروف العربية","تعلم شكل وصوت الحرف"),("الحركات","الفتحة والضمة والكسرة"),("المقاطع","دمج الأصوات في مقاطع"),("الكلمات الأولى","قراءة كلمات بسيطة"),("الجملة","بناء جملة عربية قصيرة")]
            english=[("English Alphabet","Learn letters and sounds"),("Phonics","Connect sounds to letters"),("CVC Words","Read simple words"),("First Sentences","Build short sentences"),("Listening","Understand simple speech")]
            for level,(title,body) in enumerate(arabic): lessons.append(Lesson(language="ar",level=level,title=title,skill="reading",body=body))
            for level,(title,body) in enumerate(english): lessons.append(Lesson(language="en",level=level,title=title,skill="reading",body=body))
            s.add_all(lessons)
        if s.query(Word).count() == 0:
            ar=[("أب","father","هذا أبي."),("أم","mother","هذه أمي."),("بيت","house","هذا بيت."),("كتاب","book","هذا كتاب."),("قلم","pen","هذا قلم."),("ماء","water","أشرب الماء.")]
            en=[("cat","قطة","The cat is here."),("dog","كلب","The dog is big."),("book","كتاب","This is a book."),("pen","قلم","This is a pen."),("water","ماء","I drink water."),("sun","شمس","The sun is bright.")]
            s.add_all([Word(language="ar",text=a,meaning=b,example=c,level=0) for a,b,c in ar])
            s.add_all([Word(language="en",text=a,meaning=b,example=c,level=0) for a,b,c in en])
        s.commit()
