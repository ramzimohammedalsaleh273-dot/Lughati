"""مؤلف المحتوى التعليمي للدفعة الأولى: 13 مستوى × 6 مهارات × دروس وأنشطة وتقويم وقصص."""
from app.first_half_content import AR_VOCAB, EN_VOCAB

SKILLS=("listening","speaking","reading","writing","vocabulary","grammar")
AGE_GROUPS=("4–5","6–7","8–10","11–13","14+")

AR_LEVELS=[
("التهيئة والأصوات","الوعي السمعي والصوتي","يميز أصواتاً مألوفة ويستجيب لتعليمات قصيرة."),
("الحروف وأشكالها","الحروف","يربط الحرف بصوته وشكله ويكتبه بصورة صحيحة."),
("الحركات والمقاطع","الحركات والمدود","يقرأ المقاطع المشكولة ويميز الحركة والمد."),
("الكلمات الأساسية","المفردات والقراءة","يقرأ كلمات يومية ويفهمها في جمل قصيرة."),
("الجملة الاسمية","الجملة والفهم","يبني جملاً اسمية ويصف أشخاصاً وأشياء."),
("الجملة الفعلية","الأفعال","يستخدم الفعل والفاعل للتعبير عن أحداث يومية."),
("القراءة والفهم","النصوص القصيرة","يستخرج الفكرة والتفاصيل من نص بسيط."),
("الإملاء والكتابة","الإملاء","يكتب كلمات وجملاً من السماع والنسخ والذاكرة."),
("النحو الأساسي","الضمائر وحروف الجر","يوظف الضمائر وحروف الجر في سياقات عملية."),
("التعبير والمحادثة","التواصل","يتحدث ويكتب عن نفسه وروتينه وبيئته."),
("النحو المتوسط","التراكيب","يطبق قواعد متوسطة داخل نصوص لا في أمثلة معزولة."),
("القراءة المتقدمة","التحليل والاستنتاج","يحلل النص ويستنتج المعنى ويلخصه."),
("الإتقان والتطبيق","الطلاقة الوظيفية","يستخدم العربية في مواقف تعليمية وحياتية متنوعة."),
]
EN_LEVELS=[
("Getting Ready","listening and phonemic awareness","Identify familiar sounds and follow short instructions."),
("Alphabet","letters and sounds","Connect letters, sounds and written forms."),
("Phonics and Blending","short vowels and blending","Read and spell simple syllables and CVC words."),
("Core Vocabulary","everyday vocabulary","Read useful words and use them in short sentences."),
("Simple Sentences","sentence patterns","Build and understand clear simple sentences."),
("Grammar Basics","verbs and subjects","Describe everyday actions with basic grammar."),
("Reading","short texts","Find main ideas and supporting details."),
("Writing","spelling and paragraphs","Write dictated words, sentences and short paragraphs."),
("Grammar in Context","pronouns and prepositions","Use grammar accurately in meaningful contexts."),
("Speaking","conversation","Talk about routines, needs, preferences and places."),
("Intermediate Grammar","accuracy and connectors","Apply intermediate structures in connected language."),
("Advanced Reading","analysis and inference","Infer meaning, analyze and summarize longer texts."),
("Functional Mastery","real-life communication","Use English effectively in practical situations."),
]

AR_SKILL_TASKS={
"listening":"استمع إلى المثال ثم حدد الصوت أو الكلمة المطلوبة.",
"speaking":"انطق المثال بصوت واضح ثم عبّر بجملة من إنشائك.",
"reading":"اقرأ النص ببطء ثم أجب عن سؤال الفهم.",
"writing":"اكتب المثال من الذاكرة ثم قارنه بالنموذج.",
"vocabulary":"تعلم الكلمة الجديدة واستعملها في جملة مفيدة.",
"grammar":"طبّق القاعدة في مثال جديد من حياتك اليومية.",
}
EN_SKILL_TASKS={
"listening":"Listen to the model and identify the requested sound or word.",
"speaking":"Say the model aloud and produce your own sentence.",
"reading":"Read the short text and answer the comprehension question.",
"writing":"Write the model from memory and compare it with the answer.",
"vocabulary":"Learn the new word and use it in a meaningful sentence.",
"grammar":"Apply the grammar pattern to a new real-life example.",
}

def _age_instruction(language,age):
    if language=="ar":
        return {
            "4–5":"نشاط قصير مع صور وحركة وتكرار شفهي.",
            "6–7":"نشاط قصير مع قراءة ونسخ وتكرار موجّه.",
            "8–10":"نشاط مستقل مع مثال ثم تطبيق جديد.",
            "11–13":"نشاط قائم على الفهم والتفسير والتطبيق.",
            "14+":"نشاط وظيفي يربط اللغة بموقف واقعي.",
        }[age]
    return {
        "4–5":"Short activity using pictures, movement and oral repetition.",
        "6–7":"Short activity with guided reading, copying and repetition.",
        "8–10":"Independent task with a model followed by new practice.",
        "11–13":"Task focused on understanding, explanation and application.",
        "14+":"Functional task connected to a realistic situation.",
    }[age]

def _lesson(language,level,skill,theme,objective,age):
    if language=="ar":
        task=AR_SKILL_TASKS[skill]
        title=f"{theme} — {skill}"
        body=f"الهدف: {objective}\n\n{task}\n\nالفئة العمرية: {age}. {_age_instruction(language,age)}"
        activities=[
            ("تهيئة",f"راجع المعرفة السابقة المرتبطة بموضوع {theme}."),
            ("نموذج",task),
            ("تطبيق",f"أنجز مهمة جديدة دون نسخ المثال، ثم صحح أخطاءك. ({age})"),
            ("تقويم","أعد المهمة في مثال مختلف وتحقق من تحقق الهدف."),
        ]
    else:
        task=EN_SKILL_TASKS[skill]
        title=f"{theme} — {skill.title()}"
        body=f"Goal: {objective}\n\n{task}\n\nAge group: {age}. {_age_instruction(language,age)}"
        activities=[
            ("Warm-up",f"Review prior knowledge connected to {theme}."),
            ("Model",task),
            ("Practice",f"Complete a new task without copying the model, then correct mistakes. ({age})"),
            ("Assessment","Repeat the skill with a different example and check the outcome."),
        ]
    return {"language":language,"level":level,"title":title,"skill":skill,"body":body,
            "age_group":age,"activities":[{"kind":k,"instruction":i} for k,i in activities]}

def _questions(language,level,words):
    w1,w2,w3=words[:3]
    if language=="ar":
        return [
            {"language":"ar","level":level,"skill":"listening","type":"listening","prompt":f"اكتب الكلمة التي تسمعها: «{w2[0]}».","options":[],"answer":w2[0]},
            {"language":"ar","level":level,"skill":"speaking","type":"speaking","prompt":f"تحدث بجملة مفيدة عن «{w3[0]}».","options":[],"answer":"تقييم ذاتي"},
            {"language":"ar","level":level,"skill":"reading","type":"mcq","prompt":f"ما الكلمة المرتبطة بالموضوع في المثال؟","options":[w1[0],w2[0],w3[0]],"answer":w1[0]},
            {"language":"ar","level":level,"skill":"writing","type":"writing","prompt":f"اكتب كلمة «{w1[0]}» كتابة صحيحة.","options":[],"answer":w1[0]},
            {"language":"ar","level":level,"skill":"vocabulary","type":"mcq","prompt":f"ما معنى «{w1[0]}»؟","options":[w1[1],w2[1],w3[1]],"answer":w1[1]},
            {"language":"ar","level":level,"skill":"grammar","type":"true_false","prompt":"استخدام الكلمة داخل جملة مفيدة يساعد على فهم وظيفتها.","options":["صحيح","خطأ"],"answer":"صحيح"},
            {"language":"ar","level":level,"skill":"reading","type":"mcq","prompt":"أي خيار يمثل قراءة وفهماً لا حفظاً فقط؟","options":["استخراج فكرة من النص","تكرار عنوان فقط","تجاهل السؤال"],"answer":"استخراج فكرة من النص"},
            {"language":"ar","level":level,"skill":"grammar","type":"true_false","prompt":"ينبغي تطبيق القاعدة في سياق جديد للتأكد من فهمها.","options":["صحيح","خطأ"],"answer":"صحيح"},
            {"language":"ar","level":level,"skill":"vocabulary","type":"mcq","prompt":f"اختر الكلمة المختلفة عن «{w1[0]}» في المعنى.","options":[w1[0],w2[0],w3[0]],"answer":w2[0]},
            {"language":"ar","level":level,"skill":"writing","type":"writing","prompt":f"اكتب مثالاً يحتوي على «{w2[0]}».","options":[],"answer":w2[0]},
            {"language":"ar","level":level,"skill":"listening","type":"listening","prompt":f"اكتب الكلمة المسموعة الثانية: «{w3[0]}».","options":[],"answer":w3[0]},
            {"language":"ar","level":level,"skill":"speaking","type":"speaking","prompt":"لخص ما تعلمته اليوم بجملتين.","options":[],"answer":"تقييم ذاتي"},
        ]
    return [
        {"language":"en","level":level,"skill":"listening","type":"listening","prompt":f"Type the word you hear: “{w2[0]}”.","options":[],"answer":w2[0]},
        {"language":"en","level":level,"skill":"speaking","type":"speaking","prompt":f"Say one useful sentence about “{w3[0]}”.","options":[],"answer":"self assessment"},
        {"language":"en","level":level,"skill":"reading","type":"mcq","prompt":"Which word is part of the lesson vocabulary?","options":[w1[0],w2[0],w3[0]],"answer":w1[0]},
        {"language":"en","level":level,"skill":"writing","type":"writing","prompt":f"Write the word “{w1[0]}” correctly.","options":[],"answer":w1[0]},
        {"language":"en","level":level,"skill":"vocabulary","type":"mcq","prompt":f"What does “{w1[0]}” mean?","options":[w1[1],w2[1],w3[1]],"answer":w1[1]},
        {"language":"en","level":level,"skill":"grammar","type":"true_false","prompt":"Applying a grammar pattern in a new context demonstrates understanding.","options":["True","False"],"answer":"True"},
        {"language":"en","level":level,"skill":"reading","type":"mcq","prompt":"Which action shows reading comprehension?","options":["Finding an idea in a text","Repeating a title only","Ignoring the question"],"answer":"Finding an idea in a text"},
        {"language":"en","level":level,"skill":"grammar","type":"true_false","prompt":"A learner should use a grammar rule in a new context to check understanding.","options":["True","False"],"answer":"True"},
        {"language":"en","level":level,"skill":"vocabulary","type":"mcq","prompt":f"Choose a different vocabulary item from “{w1[0]}”.","options":[w1[0],w2[0],w3[0]],"answer":w2[0]},
        {"language":"en","level":level,"skill":"writing","type":"writing","prompt":f"Write a sentence containing “{w2[0]}”.","options":[],"answer":w2[0]},
        {"language":"en","level":level,"skill":"listening","type":"listening","prompt":f"Type the second heard word: “{w3[0]}”.","options":[],"answer":w3[0]},
        {"language":"en","level":level,"skill":"speaking","type":"speaking","prompt":"Summarize what you learned today in two sentences.","options":[],"answer":"self assessment"},
    ]

def build_content():
    lessons=[]; words=[]; stories=[]; questions=[]
    for language,levels,vocab in (("ar",AR_LEVELS,AR_VOCAB),("en",EN_LEVELS,EN_VOCAB)):
        for level,(title,theme,objective) in enumerate(levels):
            selected=[vocab[(level*7+i)%len(vocab)] for i in range(12)]
            for term,meaning,example in selected:
                words.append({"language":language,"text":term,"meaning":meaning,"example":example,"level":level})
            for age in AGE_GROUPS:
                # العمر يغير إرشادات الدرس، بينما يبقى ناتج التعلم نفسه.
                if age=="14+":
                    for skill in SKILLS:
                        lessons.append(_lesson(language,level,skill,theme,objective,age))
                else:
                    # نحفظ نفس المهارات الأساسية لكل عمر دون مضاعفة المنهج بلا حاجة.
                    pass
            stories.append({
                "language":language,"level":level,
                "title":f"قصة المستوى {level}: {title}" if language=="ar" else f"Level {level} Story: {title}",
                "body":(
                    f"قصة تدريبية عن {theme}. {selected[0][0]} و{selected[1][0]} يظهران في موقف يومي. "
                    f"يقرأ المتعلم الفقرة، يحدد الفكرة، ثم يجيب عن سؤال ويعيد سردها."
                    if language=="ar" else
                    f"A short story about {theme}. {selected[0][0]} and {selected[1][0]} appear in a daily situation. "
                    f"The learner reads, identifies the main idea, answers a question, and retells it."
                )
            })
            questions.extend(_questions(language,level,selected))
    return lessons,words,stories,questions
