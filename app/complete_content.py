"""حزمة المحتوى الموسعة: مناهج مستقلة للفئات العمرية الخمس + دروس + أنشطة + قصص + تقويم."""
from app.models import CurriculumUnit
from app.first_half_content import AR_VOCAB, EN_VOCAB
from app.curriculum_engine import AGE_GROUPS, SKILLS, level_title

AGE_RULES={
"4–5":{"ar":"تعلم بالصور والحركة والتكرار الشفهي، مع نشاط قصير لا يتجاوز 10 دقائق.","en":"Learn through pictures, movement and oral repetition; keep each activity under 10 minutes."},
"6–7":{"ar":"قراءة وكتابة موجّهة مع تكرار صوتي وأمثلة محسوسة.","en":"Guided reading and writing with repeated audio and concrete examples."},
"8–10":{"ar":"تدريب مستقل تدريجي يجمع الفهم والتطبيق والمراجعة.","en":"Gradual independent practice combining understanding, application and review."},
"11–13":{"ar":"تحليل وتفسير وتطبيق في نصوص ومواقف متنوعة.","en":"Analysis, explanation and application across varied texts and situations."},
"14+":{"ar":"تطبيق وظيفي واقعي مع استقلالية ومهام أداء.","en":"Real-world functional practice with independent performance tasks."},
}
SKILL_TEXT={
"listening":{"ar":"استمع للنموذج ثم حدّد الفكرة أو الصوت أو الكلمة، وأعد الاستماع بسرعة أبطأ ثم طبيعية.","en":"Listen to the model, identify the sound, word or idea, then replay slowly and naturally."},
"speaking":{"ar":"استمع للنموذج، كرر، ثم أنشئ جملة جديدة وسجّلها للمقارنة.","en":"Listen, repeat, create a new sentence, and record yourself for comparison."},
"reading":{"ar":"اقرأ النص مرتين: مرة للفهم ومرة لاستخراج التفاصيل، ثم أجب عن أسئلة الاستنتاج.","en":"Read twice: once for meaning and once for details, then answer inference questions."},
"writing":{"ar":"شاهد النموذج، انسخه، ثم اكتبه من الذاكرة، وبعدها أصلح الأخطاء وفسّرها.","en":"Study the model, copy it, write it from memory, then correct and explain errors."},
"vocabulary":{"ar":"تعلّم الكلمة مع معناها وصورتها وسياقها ونطقها، ثم استخدمها في جملتين.","en":"Learn the word with meaning, image, context and pronunciation, then use it in two sentences."},
"grammar":{"ar":"اكتشف القاعدة من أمثلة، طبّقها في أمثلة جديدة، ثم اشرح سبب صحة الإجابة.","en":"Discover the rule from examples, apply it to new examples, and explain why it is correct."},
}
THEMES={"ar":["الأسرة","المدرسة","الألوان والأشكال","البيت","الطعام","الجسم والصحة","الطبيعة","الحيوانات","المدينة","الوقت والروتين","السفر","التقنية","الحياة والمجتمع"],
"en":["Family","School","Colors and Shapes","Home","Food","Body and Health","Nature","Animals","City","Time and Routines","Travel","Technology","Life and Society"]}
AR_EXTRA_WORDS="""كتاب قلم دفتر مدرسة معلم طالب فصل درس سؤال جواب بيت غرفة مطبخ حديقة شارع مدينة قرية سوق متجر مستشفى حافلة قطار طائرة سفينة دراجة هاتف حاسوب شاشة لوحة مفتاح حقيبة حذاء قميص بنطال قبعة لون أحمر أزرق أخضر أصفر أبيض أسود برتقالي دائري مربع طويل قصير كبير صغير قريب بعيد فوق تحت أمام خلف داخل خارج يمين يسار صباح مساء ليل نهار أسبوع شهر سنة الآن لاحقاً قبل بعد اليوم غداً أمس أول آخر بداية نهاية سريع بطيء سهل صعب صحيح خطأ جميل قبيح قوي ضعيف سعيد حزين هادئ نشيط جائع عطشان حار بارد نظيف متسخ جديد قديم مفتوح مغلق يقرأ يكتب يسمع يتكلم يرى يعرف يفهم يتعلم يدرس يعمل يساعد يحب يريد يحتاج يعطي يأخذ يذهب يأتي يجلس يقف يركض يمشي يلعب ينام يستيقظ يأكل يشرب يفتح يغلق يبدأ ينتهي يسأل يجيب يشرح يختار يرتب يقارن يصف يحكي يلخص يستنتج يفكر يتذكر ينسى يتدرب ينجح يحاول يصلح يخطط ينظم يتعاون يشارك ينتظر يستخدم يصنع يشتري يبيع يدفع يعيش يسافر يعود يزور""".split()
EN_EXTRA_WORDS="""book pen notebook school teacher student class lesson question answer house room kitchen garden street city village market shop hospital bus train plane ship bicycle phone computer screen keyboard key bag shoe shirt trousers hat color red blue green yellow white black orange round square long short big small near far above below before behind inside outside right left morning evening night day week month year now later today tomorrow yesterday first last beginning end fast slow easy difficult correct wrong beautiful ugly strong weak happy sad quiet active hungry thirsty hot cold clean dirty new old open closed read write hear speak see know understand learn study work help love want need give take go come sit stand run walk play sleep wake eat drink start finish ask explain choose arrange compare describe tell summarize infer think remember forget practice succeed try fix plan organize cooperate share wait use make buy sell pay live travel return visit""".split()
def _words(language):
    base=AR_VOCAB if language=="ar" else EN_VOCAB; extras=AR_EXTRA_WORDS if language=="ar" else EN_EXTRA_WORDS
    seen=set(); out=[]
    for term,meaning,example in base:
        if term not in seen: out.append((term,meaning,example)); seen.add(term)
    for term in extras:
        if term in seen: continue
        meaning=term
        example=(f"أستخدم كلمة «{term}» في جملة مفيدة." if language=="ar" else f"I use the word {term} in a useful sentence.")
        out.append((term,meaning,example)); seen.add(term)
    return out
def build_age_units():
    rows=[]
    for lang in ("ar","en"):
        for age in AGE_GROUPS:
            for level in range(13):
                theme=THEMES[lang][level]; title=level_title(lang,level)
                for skill in SKILLS:
                    goal=SKILL_TEXT[skill][lang]; age_rule=AGE_RULES[age][lang]
                    if lang=="ar":
                        body=f"المستوى {level}: {title}\nالموضوع: {theme}\nالمهارة: {skill}\n\nهدف الدرس: {goal}\n\nالتكييف العمري ({age}): {age_rule}\n\nالتسلسل: تهيئة ← نموذج ← تدريب موجّه ← تدريب مستقل ← تقويم ← مراجعة متباعدة."
                        activity=f"أنجز نشاط {skill} حول موضوع {theme} للفئة {age}، ثم قدّم دليلاً على الإتقان."
                    else:
                        body=f"Level {level}: {title}\nTheme: {theme}\nSkill: {skill}\n\nLesson goal: {goal}\n\nAge adaptation ({age}): {age_rule}\n\nSequence: warm-up → model → guided practice → independent practice → assessment → spaced review."
                        activity=f"Complete the {skill} activity about {theme} for age group {age}, then provide evidence of mastery."
                    rows.append({"language":lang,"age_group":age,"level":level,"skill":skill,"title":f"{title} — {theme} — {skill} — {age}","body":body,"activity":activity})
    return rows
def build_extended_words():
    rows=[]
    for lang in ("ar","en"):
        vocab=_words(lang)
        for level in range(13):
            start=(level*17)%len(vocab)
            for i in range(min(35,len(vocab))):
                term,meaning,example=vocab[(start+i)%len(vocab)]
                rows.append({"language":lang,"text":term,"meaning":meaning,"example":example,"level":level})
    return rows
def build_age_stories():
    rows=[]
    for lang in ("ar","en"):
        for age in AGE_GROUPS:
            for level in range(13):
                theme=THEMES[lang][level]
                if lang=="ar":
                    title=f"قصة {theme} — المستوى {level} — {age}"
                    body=f"في قصة اليوم نتعلم عن {theme}. يواجه المتعلم موقفاً مناسباً للفئة {age}. يستمع أو يقرأ، يختار قراراً، يجيب عن أسئلة الفهم، ثم يعيد سرد القصة بكلماته."
                    questions=[{"prompt":"ما الفكرة الرئيسية في القصة؟","options":["الموقف والتعلم","لا شيء","حذف القصة"],"answer":"الموقف والتعلم"},{"prompt":"اذكر دليلاً من القصة.","options":[],"answer":"إجابة مفتوحة"}]
                else:
                    title=f"{theme} Story — Level {level} — {age}"
                    body=f"Today's story is about {theme}. The learner meets an age-appropriate situation for {age}, makes a choice, answers comprehension questions, and retells it in their own words."
                    questions=[{"prompt":"What is the main idea?","options":["The situation and learning","Nothing","Delete the story"],"answer":"The situation and learning"},{"prompt":"Give one detail from the story.","options":[],"answer":"open response"}]
                rows.append({"language":lang,"level":level,"age_group":age,"title":title,"body":body,"questions":questions})
    return rows
