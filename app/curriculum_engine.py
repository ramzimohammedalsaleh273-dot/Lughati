"""محرك المنهج: يعرّف بنية 13 مستوى ومخرجات قابلة للقياس لكل لغة وفئة عمرية."""
from dataclasses import dataclass

AGE_GROUPS=("4–5","6–7","8–10","11–13","14+")
SKILLS=("listening","speaking","reading","writing","vocabulary","grammar")

@dataclass(frozen=True)
class Outcome:
    level:int
    language:str
    skill:str
    objective:str
    evidence:str

AR_OUTCOMES = {
0:["يميز الأصوات الأساسية","يكرر أصواتاً وكلمات قصيرة","يتعرف الحروف بصرياً","يمسك القلم ويقلد خطوطاً بسيطة","يفهم مفردات الأسرة والأشياء","يميز الاسم عن الفعل في أمثلة بسيطة"],
1:["يميز أصوات الحروف","ينطق الحروف بوضوح","يربط الحرف بصورته","ينسخ الحروف","يبني حصيلة الحروف والكلمات","يميز الاسم والفعل"],
2:["يميز الحركات","ينطق المقاطع","يقرأ مقاطع مشكولة","يكتب مقاطع قصيرة","يفهم كلمات مشكلة","يميز أنماطاً نحوية بسيطة"],
3:["يفهم كلمات مسموعة","يستخدم كلمات يومية","يقرأ كلمات مألوفة","يكتب كلمات من الإملاء","يوظف مفردات يومية","يميز المفرد والجمع في أمثلة"],
4:["يفهم جملاً قصيرة","يجيب بجمل بسيطة","يقرأ جملاً","يكتب جملاً اسمية","يوسع مفرداته","يبني جملة اسمية سليمة"],
5:["يفهم أفعالاً يومية","يصف نشاطاً يومياً","يقرأ جملاً فعلية","يكتب جملاً فعلية","يستخدم أفعالاً شائعة","يميز الفعل والفاعل"],
6:["يفهم نصاً قصيراً","يعيد سرد فكرة","يحدد الفكرة الرئيسية","يكتب إجابة قصيرة","يستخرج مفردات السياق","يميز التفاصيل والجمل"],
7:["يفهم الإملاء المسموع","يصف ما يراه","يقرأ نصاً قصيراً","يكتب فقرة قصيرة","يستخدم مفردات مترابطة","يطبق علامات الوقف الأساسية"],
8:["يفهم الضمائر في الكلام","يستخدم الضمائر","يقرأ تراكيب متنوعة","يكتب جملاً مترابطة","يوظف حروف الجر","يطبق الضمائر وحروف الجر"],
9:["يفهم حواراً يومياً","يدير محادثة قصيرة","يقرأ حواراً","يكتب وصفاً","يستخدم مفردات المواقف","يبني تراكيب صحيحة"],
10:["يفهم تراكيب متوسطة","يتحدث بدقة أكبر","يحلل فقرة","يكتب فقرة مترابطة","يفرق المفردات المتقاربة","يطبق قواعد متوسطة في السياق"],
11:["يفهم المعنى الضمني","يقدم استنتاجاً شفهياً","يحلل نصاً","يلخص نصاً","يفهم المفردات من السياق","يحلل التراكيب والحجج"],
12:["يفهم مواقف الحياة","يتحدث بطلاقة وظيفية","يقرأ نصوصاً متنوعة","يكتب نصاً وظيفياً","يوظف مفردات واسعة","يستخدم القواعد بدقة عملية"],
}
EN_OUTCOMES = {
0:["identify common sounds","repeat basic sounds and words","recognize letters visually","copy simple lines and forms","understand family and object words","notice nouns and verbs"],
1:["identify letter sounds","pronounce letters clearly","connect letters to symbols","write letters","build letter vocabulary","distinguish basic word classes"],
2:["identify short vowels","blend simple syllables","read CVC words","spell short words","understand basic vocabulary","notice simple grammar patterns"],
3:["understand everyday words","use basic spoken words","read familiar words","write dictated words","build everyday vocabulary","notice singular and plural"],
4:["understand short sentences","answer in simple sentences","read simple sentences","write simple sentences","expand vocabulary","build correct sentence patterns"],
5:["understand common verbs","describe routines","read verb sentences","write verb sentences","use common verbs","identify subject and verb"],
6:["understand short texts","retell a main idea","find main ideas","write short answers","infer vocabulary from context","identify supporting details"],
7:["understand dictated text","describe familiar scenes","read short passages","write short paragraphs","connect related words","use basic punctuation"],
8:["understand pronouns in context","use pronouns in speech","read varied patterns","write connected sentences","use prepositions","apply pronouns and prepositions"],
9:["understand daily dialogues","hold short conversations","read dialogues","write descriptions","use situation vocabulary","build accurate patterns"],
10:["understand intermediate structures","speak with greater accuracy","analyze a paragraph","write connected paragraphs","distinguish close meanings","apply grammar in context"],
11:["infer implied meaning","explain an inference","analyze longer texts","summarize texts","infer vocabulary from context","analyze structures and arguments"],
12:["understand real-life situations","communicate functionally","read varied practical texts","write functional texts","use broad practical vocabulary","use grammar accurately in context"],
}

def outcomes(language, level, age_group=None):
    level=max(0,min(12,int(level)))
    data=AR_OUTCOMES if language=="ar" else EN_OUTCOMES
    objectives=data[level]
    if age_group is None: age_group="14+"
    return [Outcome(level,language,skill,obj,f"مهمة أداء + سؤال تقويمي + ملاحظة تقدم" if language=="ar" else "performance task + assessment item + progress evidence") for skill,obj in zip(SKILLS,objectives)]

def level_title(language,level):
    ar=["التهيئة والأصوات","الحروف وأشكالها","الحركات والمقاطع","الكلمات الأساسية","الجملة الاسمية","الجملة الفعلية","القراءة والفهم","الإملاء والكتابة","النحو الأساسي","التعبير والمحادثة","النحو المتوسط","القراءة المتقدمة","الإتقان والتطبيق"]
    en=["Getting Ready","Alphabet","Phonics and Blending","Core Vocabulary","Simple Sentences","Grammar Basics","Reading","Writing","Grammar in Context","Speaking","Intermediate Grammar","Advanced Reading","Functional Mastery"]
    return (ar if language=="ar" else en)[max(0,min(12,int(level)))]

def curriculum_matrix(language):
    return {level:outcomes(language,level) for level in range(13)}
