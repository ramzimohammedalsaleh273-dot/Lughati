from app.services import words,stories
from app.curriculum import ARABIC_LEVELS,ENGLISH_LEVELS

def answer(query,language="ar"):
    q=query.strip().casefold()
    if not q: return "اكتب سؤالك أولاً."
    if "مستوى" in q or "level" in q:
        levels=ARABIC_LEVELS if language=="ar" else ENGLISH_LEVELS
        return "المستويات من 0 إلى 12. البداية: "+levels[0]
    if "حرف" in q or "letter" in q:
        return "ابدأ بشكل الحرف وصوته، ثم طبقه في مقطع وكلمة."
    if "مراجعة" in q or "review" in q:
        return "افتح المراجعة الذكية وأنهِ الكلمات المستحقة اليوم."
    matches=words(language,query=query)
    if matches:
        w=matches[0]; return f"الكلمة: {w.text}\nالمعنى: {w.meaning}\nمثال: {w.example}"
    if "قصة" in q or "story" in q:
        return f"لديك {len(stories(language))} قصة في هذه اللغة."
    return "أستطيع المساعدة في الدروس والمفردات والمراجعة والاختبارات.";
