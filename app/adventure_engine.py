"""محرك المغامرة التعليمية: 156 مهمة مترابطة."""
from dataclasses import dataclass
@dataclass(frozen=True)
class AdventureNode:
    id:str; language:str; level:int; title:str; skill:str; goal:str; reward:int
def build_world(language):
    skills=("listening","speaking","reading","writing","vocabulary","grammar"); nodes=[]
    for level in range(13):
        for i,skill in enumerate(skills):
            nodes.append(AdventureNode(f"{language}-{level}-{skill}",language,level,f"المهمة {level+1}: {skill}" if language=="ar" else f"Mission {level+1}: {skill}",skill,"اتقن المهارة ثم افتح المهمة التالية." if language=="ar" else "Master the skill to unlock the next mission.",10+i*2))
    return nodes
def available_nodes(language, mastered_ids):
    world=build_world(language)
    return [n for i,n in enumerate(world) if i==0 or world[i-1].id in mastered_ids]
def reward_for(score): return 3 if float(score)>=90 else 2 if float(score)>=75 else 1 if float(score)>=60 else 0
