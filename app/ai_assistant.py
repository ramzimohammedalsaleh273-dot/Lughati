"""مساعد لغوي هجين: محلي + مزود HTTP اختياري عند توفر الإنترنت."""
import json, os, urllib.request
def local_answer(prompt, language="ar"):
    p=str(prompt).strip()
    if not p: return "اكتب سؤالك أولاً." if language=="ar" else "Write your question first."
    return (f"المساعد المحلي: حوّل سؤالك «{p}» إلى: شرح مختصر، مثال، تدريب، ثم تصحيح." if language=="ar" else f"Local assistant: turn “{p}” into an explanation, example, practice task, and correction.")
def online_answer(prompt, language="ar", endpoint=None, api_key=None):
    endpoint=endpoint or os.getenv("LUGHATI_AI_ENDPOINT"); api_key=api_key or os.getenv("LUGHATI_AI_KEY")
    if not endpoint or not api_key: return None
    payload={"prompt":prompt,"language":language,"system":"You are a safe language-learning tutor. Explain, quiz, correct, and adapt to age."}
    try:
        req=urllib.request.Request(endpoint,data=json.dumps(payload,ensure_ascii=False).encode(),headers={"Content-Type":"application/json","Authorization":f"Bearer {api_key}"})
        with urllib.request.urlopen(req,timeout=20) as r: data=json.loads(r.read().decode())
        return data.get("answer") or data.get("output") or data.get("text")
    except Exception: return None
def answer(prompt, language="ar"): return online_answer(prompt,language) or local_answer(prompt,language)
