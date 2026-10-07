"""تكييف مستوى النشاط بحسب الفئة العمرية دون تغيير ناتج التعلم الأساسي."""
AGE_GROUPS=("4–5","6–7","8–10","11–13","14+")

GUIDANCE={
"4–5":{"ar":"شفهي، صور، حركة، تكرار، مهمة قصيرة.","en":"oral, pictures, movement, repetition, short task."},
"6–7":{"ar":"قراءة موجهة، نسخ، نطق، ومهمة قصيرة.","en":"guided reading, copying, pronunciation, short task."},
"8–10":{"ar":"مثال ثم تطبيق مستقل مع تصحيح ذاتي.","en":"model followed by independent practice and self-correction."},
"11–13":{"ar":"فهم، تفسير، تطبيق، ومهمة أداء.","en":"understanding, explanation, application and performance task."},
"14+":{"ar":"موقف وظيفي واقعي مع قياس واضح للمهارة.","en":"realistic functional situation with explicit skill evidence."},
}

def age_guidance(age_group,language="ar"):
    if age_group not in AGE_GROUPS: raise ValueError("الفئة العمرية غير مدعومة")
    language="ar" if language=="ar" else "en"
    return GUIDANCE[age_group][language]

def adapt_activity(instruction,age_group,language="ar"):
    return f"{instruction}\n\nالتكييف العمري: {age_guidance(age_group,language)}"

def all_age_guidance(language="ar"):
    return {age:age_guidance(age,language) for age in AGE_GROUPS}
