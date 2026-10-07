"""المحتوى التعليمي الأساسي للدفعة الأولى من لغتي.
يبني منهجاً حقيقياً قابلاً للتدريس: 13 مستوى × مهارات × أنشطة × قصص × تقويم.
"""
import json

AR_LEVEL_THEMES = [
    ("التهيئة والأصوات","الاستماع والوعي الصوتي","تمييز الأصوات من حولنا"),
    ("الحروف وأشكالها","الحروف والأصوات","التعرف إلى الحروف وكتابتها"),
    ("الحركات والمقاطع","الحركات والمقاطع","الفتحة والضمة والكسرة والمدود"),
    ("الكلمات الأساسية","المفردات والقراءة","قراءة كلمات من الحياة اليومية"),
    ("الجملة الاسمية","الجملة والفهم","بناء الجملة الاسمية ووصف الأشياء"),
    ("الجملة الفعلية","الفعل والفاعل","التعبير عن الأفعال اليومية"),
    ("القراءة والفهم","القراءة والفهم","استخراج الفكرة والتفاصيل"),
    ("الإملاء والكتابة","الإملاء والكتابة","النسخ والإملاء وكتابة الجمل"),
    ("النحو الأساسي","الضمائر وحروف الجر","استخدام التراكيب الأساسية"),
    ("التعبير والمحادثة","التحدث والتعبير","وصف الذات واليوم والمكان"),
    ("النحو المتوسط","النحو والتراكيب","تطبيق القواعد في سياق"),
    ("القراءة المتقدمة","التحليل والاستنتاج","التلخيص والاستنتاج من النص"),
    ("الإتقان والتطبيق","الطلاقة","استخدام العربية في الحياة اليومية"),
]
EN_LEVEL_THEMES = [
    ("Getting Ready","listening and phonemic awareness","hearing and identifying sounds"),
    ("Alphabet","letters and sounds","recognizing and writing letters"),
    ("Phonics and Blending","phonics and blending","short vowels and CVC words"),
    ("Core Vocabulary","vocabulary and reading","reading useful everyday words"),
    ("Simple Sentences","sentences and comprehension","building clear simple sentences"),
    ("Grammar Basics","verbs and grammar","talking about everyday actions"),
    ("Reading","reading and comprehension","finding main ideas and details"),
    ("Writing","writing and spelling","writing words and short paragraphs"),
    ("Grammar in Context","pronouns and prepositions","using grammar in real contexts"),
    ("Speaking","speaking and conversation","describing routines and preferences"),
    ("Intermediate Grammar","grammar and accuracy","using structures in context"),
    ("Advanced Reading","analysis and inference","summarizing and inferring"),
    ("Functional Mastery","fluency","using English for real-life tasks"),
]

AR_ACTIVITY_TEMPLATES = [
    ("استماع","استمع إلى أمثلة المعلم وحدد الصوت أو الكلمة المطلوبة."),
    ("تحدث","اقرأ الأمثلة بصوت واضح ثم أعدها دون النظر إلى النموذج."),
    ("قراءة","اقرأ النص القصير ببطء، ثم أجب عن سؤال الفهم."),
    ("كتابة","انسخ المثال مرة، ثم اكتبه من الذاكرة، ثم راجعه."),
    ("مفردات","تعلم الكلمات الجديدة واستعمل كل كلمة في جملة."),
    ("تقويم","حل سؤالاً جديداً يختبر المهارة نفسها في سياق مختلف."),
]
EN_ACTIVITY_TEMPLATES = [
    ("Listening","Listen to the examples and identify the requested sound or word."),
    ("Speaking","Read the examples aloud, then repeat them without the model."),
    ("Reading","Read the short text and answer the comprehension question."),
    ("Writing","Copy the example, write it from memory, then check it."),
    ("Vocabulary","Learn the new words and use each word in a sentence."),
    ("Assessment","Answer a new item that checks the same skill in context."),
]

AR_VOCAB = [
("أب","father","هذا أبي."),("أم","mother","هذه أمي."),("أخ","brother","هذا أخي."),("أخت","sister","هذه أختي."),
("بيت","house","بيتي قريب."),("باب","door","الباب مفتوح."),("نافذة","window","النافذة كبيرة."),("كتاب","book","هذا كتاب مفيد."),
("قلم","pen","هذا قلم جديد."),("دفتر","notebook","أكتب في الدفتر."),("مدرسة","school","أذهب إلى المدرسة."),("معلم","teacher","المعلم يشرح الدرس."),
("طالب","student","الطالب يقرأ."),("كرسي","chair","أجلس على الكرسي."),("طاولة","table","الكتاب على الطاولة."),("ماء","water","أشرب الماء."),
("طعام","food","الطعام لذيذ."),("تفاح","apple","أحب التفاح."),("خبز","bread","أكل الخبز."),("حليب","milk","أشرب الحليب."),
("شمس","sun","الشمس مشرقة."),("قمر","moon","القمر جميل."),("سماء","sky","السماء صافية."),("أرض","earth","نمشي على الأرض."),
("شجرة","tree","الشجرة طويلة."),("زهرة","flower","الزهرة جميلة."),("حديقة","garden","في الحديقة أشجار."),("بحر","sea","البحر واسع."),
("سيارة","car","السيارة سريعة."),("طريق","road","الطريق طويل."),("صديق","friend","صديقي يساعدني."),("أسرة","family","أسرتي تحبني."),
("ولد","boy","الولد يقرأ."),("بنت","girl","البنت تكتب."),("رجل","man","الرجل يعمل."),("امرأة","woman","المرأة تقرأ."),
("طفل","child","الطفل يلعب."),("يقرأ","reads","هو يقرأ كتاباً."),("يكتب","writes","هو يكتب كلمة."),("يذهب","goes","هو يذهب إلى المدرسة."),
("يأتي","comes","هو يأتي مبكراً."),("يجلس","sits","هو يجلس هنا."),("يقوم","stands","هو يقوم الآن."),("يأكل","eats","هو يأكل الطعام."),
("يشرب","drinks","هو يشرب الماء."),("يلعب","plays","هو يلعب في الحديقة."),("ينام","sleeps","الطفل ينام."),("كبير","big","البيت كبير."),
("صغير","small","القلم صغير."),("جميل","beautiful","المنظر جميل."),("جديد","new","هذا كتاب جديد."),("قديم","old","هذا بيت قديم."),
("سريع","fast","السيارة سريعة."),("بطيء","slow","السلحفاة بطيئة."),("اليوم","today","أتعلم اليوم."),("غداً","tomorrow","سأقرأ غداً."),
("أمس","yesterday","قرأت أمس."),("صباح","morning","أدرس في الصباح."),("مساء","evening","أراجع في المساء."),("واحد","one","لدي كتاب واحد."),
("اثنان","two","لدي قلمان."),("ثلاثة","three","لدي ثلاثة كتب."),("أربعة","four","أرى أربعة أقلام."),("خمسة","five","لدي خمسة كتب."),
("أين","where","أين الكتاب؟"),("متى","when","متى نبدأ؟"),("كيف","how","كيف حالك؟"),("لماذا","why","لماذا نتعلم؟"),
("نعم","yes","نعم، فهمت."),("لا","no","لا، لم أفهم."),("لغة","language","العربية لغة جميلة."),("تعلم","learning","التعلم مستمر."),
("قراءة","reading","القراءة مفيدة."),("كتابة","writing","الكتابة تدريب."),("استماع","listening","الاستماع مهم."),("تحدث","speaking","التحدث ممارسة."),
("فكرة","idea","هذه فكرة جيدة."),("سؤال","question","لدي سؤال."),("إجابة","answer","هذه إجابة صحيحة."),("درس","lesson","بدأ الدرس."),
("وقت","time","حان وقت التعلم."),("مكان","place","هذا مكان هادئ."),("عمل","work","العمل يحتاج تركيزاً."),("هدف","goal","هدفي أن أتعلم.")
]

EN_VOCAB = [
("father","أب","My father is here."),("mother","أم","My mother is here."),("brother","أخ","My brother reads."),("sister","أخت","My sister writes."),
("house","بيت","This is my house."),("door","باب","The door is open."),("window","نافذة","The window is large."),("book","كتاب","This is a useful book."),
("pen","قلم","This is a new pen."),("notebook","دفتر","I write in my notebook."),("school","مدرسة","I go to school."),("teacher","معلم","The teacher explains."),
("student","طالب","The student reads."),("chair","كرسي","I sit on the chair."),("table","طاولة","The book is on the table."),("water","ماء","I drink water."),
("food","طعام","The food is good."),("apple","تفاح","I like apples."),("bread","خبز","I eat bread."),("milk","حليب","I drink milk."),
("sun","شمس","The sun is bright."),("moon","قمر","The moon is beautiful."),("sky","سماء","The sky is clear."),("earth","أرض","We walk on earth."),
("tree","شجرة","The tree is tall."),("flower","زهرة","The flower is beautiful."),("garden","حديقة","There are trees in the garden."),("sea","بحر","The sea is wide."),
("car","سيارة","The car is fast."),("road","طريق","The road is long."),("friend","صديق","My friend helps me."),("family","أسرة","My family loves me."),
("boy","ولد","The boy reads."),("girl","بنت","The girl writes."),("man","رجل","The man works."),("woman","امرأة","The woman reads."),
("child","طفل","The child plays."),("read","يقرأ","I read a book."),("write","يكتب","I write a word."),("go","يذهب","I go to school."),
("come","يأتي","I come early."),("sit","يجلس","I sit here."),("stand","يقوم","I stand now."),("eat","يأكل","I eat food."),
("drink","يشرب","I drink water."),("play","يلعب","I play in the garden."),("sleep","ينام","The child sleeps."),("big","كبير","The house is big."),
("small","صغير","The pen is small."),("beautiful","جميل","The view is beautiful."),("new","جديد","This is a new book."),("old","قديم","This is an old house."),
("fast","سريع","The car is fast."),("slow","بطيء","The turtle is slow."),("today","اليوم","I learn today."),("tomorrow","غداً","I will read tomorrow."),
("yesterday","أمس","I read yesterday."),("morning","صباح","I study in the morning."),("evening","مساء","I review in the evening."),("one","واحد","I have one book."),
("two","اثنان","I have two pens."),("three","ثلاثة","I have three books."),("four","أربعة","I see four pens."),("five","خمسة","I have five books."),
("where","أين","Where is the book?"),("when","متى","When do we start?"),("how","كيف","How are you?"),("why","لماذا","Why do we learn?"),
("yes","نعم","Yes, I understand."),("no","لا","No, I do not understand."),("language","لغة","English is a language."),("learning","تعلم","Learning continues."),
("reading","قراءة","Reading is useful."),("writing","كتابة","Writing is practice."),("listening","استماع","Listening is important."),("speaking","تحدث","Speaking is practice."),
("idea","فكرة","That is a good idea."),("question","سؤال","I have a question."),("answer","إجابة","This is the correct answer."),("lesson","درس","The lesson started."),
("time","وقت","It is learning time."),("place","مكان","This is a quiet place."),("work","عمل","Work needs focus."),("goal","هدف","My goal is to learn.")
]

def level_data(language, level):
    if language == "ar":
        title, skill, theme = AR_LEVEL_THEMES[level]
        return title, skill, theme
    title, skill, theme = EN_LEVEL_THEMES[level]
    return title, skill, theme

def build_rich_content():
    lessons=[]; stories=[]; questions=[]; words=[]
    for language in ("ar","en"):
        vocab=AR_VOCAB if language=="ar" else EN_VOCAB
        activities=AR_ACTIVITY_TEMPLATES if language=="ar" else EN_ACTIVITY_TEMPLATES
        for level in range(13):
            title, skill, theme = level_data(language, level)
            for idx,(kind, instruction) in enumerate(activities):
                lessons.append({
                    "language":language,"level":level,
                    "title":f"{title} — {kind}",
                    "skill":kind.lower() if language=="ar" else kind.lower(),
                    "body":f"{theme}.\n\n{instruction}\n\nالمطلوب: أن ينجز المتعلم النشاط ثم يراجع أخطاءه." if language=="ar"
                    else f"{theme}.\n\n{instruction}\n\nGoal: complete the activity and review mistakes."
                })
            chosen=vocab[(level*6)%len(vocab):(level*6)%len(vocab)+10]
            if len(chosen)<10: chosen=(vocab[(level*6)%len(vocab):]+vocab)[:10]
            for j,(term,meaning,example) in enumerate(chosen):
                words.append({"language":language,"text":term,"meaning":meaning,"example":example,"level":level})
            if language=="ar":
                body=f"في المستوى {level}: {theme}.\n\n{chosen[0][0]} و{chosen[1][0]} و{chosen[2][0]} أمثلة يتدرب عليها المتعلم. اقرأ النص، استخرج الفكرة، ثم عبّر بجملة من إنشائك."
                questions.extend([
                    {"language":"ar","level":level,"skill":"reading","type":"mcq","prompt":f"المستوى {level}: ما الهدف الأقرب للدرس؟","options":["الفهم والتطبيق","ترك التدريب","حذف الكلمات"],"answer":"الفهم والتطبيق"},
                    {"language":"ar","level":level,"skill":"vocabulary","type":"mcq","prompt":f"المستوى {level}: ما معنى «{chosen[0][0]}»؟","options":[chosen[0][1],chosen[1][1],chosen[2][1]],"answer":chosen[0][1]},
                    {"language":"ar","level":level,"skill":"writing","type":"writing","prompt":f"المستوى {level}: اكتب كلمة «{chosen[0][0]}».","options":[],"answer":chosen[0][0]},
                    {"language":"ar","level":level,"skill":"listening","type":"listening","prompt":f"المستوى {level}: استمع ثم اكتب الكلمة المسموعة.","options":[],"answer":chosen[1][0]},
                    {"language":"ar","level":level,"skill":"grammar","type":"true_false","prompt":"الجملة المفيدة تحتاج إلى معنى واضح.","options":["صحيح","خطأ"],"answer":"صحيح"},
                    {"language":"ar","level":level,"skill":"speaking","type":"speaking","prompt":f"تحدث عن «{chosen[2][0]}» بجملة واحدة.","options":[],"answer":"تقييم ذاتي"}
                ])
                stories.append({"language":"ar","level":level,"title":f"قصة المستوى {level}: {title}","body":body})
            else:
                body=f"Level {level}: {theme}.\n\nWords such as {chosen[0][0]}, {chosen[1][0]}, and {chosen[2][0]} are used in context. Read the text, find the idea, and make your own sentence."
                questions.extend([
                    {"language":"en","level":level,"skill":"reading","type":"mcq","prompt":f"Level {level}: What is the main goal?","options":["Understanding and practice","Stop training","Delete words"],"answer":"Understanding and practice"},
                    {"language":"en","level":level,"skill":"vocabulary","type":"mcq","prompt":f"Level {level}: What does “{chosen[0][0]}” mean?","options":[chosen[0][1],chosen[1][1],chosen[2][1]],"answer":chosen[0][1]},
                    {"language":"en","level":level,"skill":"writing","type":"writing","prompt":f"Level {level}: Write the word “{chosen[0][0]}”.","options":[],"answer":chosen[0][0]},
                    {"language":"en","level":level,"skill":"listening","type":"listening","prompt":f"Level {level}: Listen and type the word.","options":[],"answer":chosen[1][0]},
                    {"language":"en","level":level,"skill":"grammar","type":"true_false","prompt":"A useful sentence communicates a clear meaning.","options":["True","False"],"answer":"True"},
                    {"language":"en","level":level,"skill":"speaking","type":"speaking","prompt":f"Speak one sentence about “{chosen[2][0]}”.","options":[],"answer":"self assessment"}
                ])
                stories.append({"language":"en","level":level,"title":f"Level {level} Story: {title}","body":body})
    return lessons,words,stories,questions
