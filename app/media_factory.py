"""توليد صور تعريفية محلية. لا ننشئ ملفات WAV نغمية ونسميها صوتًا تعليميًا؛ النطق يستخدم محرك صوت النظام."""
from pathlib import Path

def ensure_media(root):
    root = Path(root)
    dirs = {key: root / key for key in ("images", "audio", "video")}
    for directory in dirs.values():
        directory.mkdir(parents=True, exist_ok=True)
    for language in ("ar", "en"):
        for level in range(13):
            label = "العربية" if language == "ar" else "اللغة الإنجليزية"
            svg = dirs["images"] / f"{language}_{level:02d}.svg"
            if not svg.exists():
                svg.write_text(
                    f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720">'
                    f'<rect width="100%" height="100%" fill="#F4F7FB"/>'
                    f'<text x="50%" y="45%" text-anchor="middle" font-size="64" '
                    f'font-family="sans-serif" fill="#27364B">{label}</text>'
                    f'<text x="50%" y="60%" text-anchor="middle" font-size="34" '
                    f'font-family="sans-serif" fill="#53657A">المستوى {level + 1}</text></svg>',
                    encoding="utf-8",
                )
    return dirs
