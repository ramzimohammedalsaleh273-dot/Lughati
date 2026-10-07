def recommended_level(score):
    score=float(score)
    if score<40:return 0
    if score<50:return 2
    if score<60:return 4
    if score<70:return 6
    if score<80:return 8
    if score<90:return 10
    return 12

def age_group(age):
    age=int(age)
    if age<=5:return "4–5"
    if age<=7:return "6–7"
    if age<=10:return "8–10"
    if age<=13:return "11–13"
    return "14+"
