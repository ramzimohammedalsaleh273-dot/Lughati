"""مولد وسائط محلية: 26 صورة SVG + 26 WAV + 26 MP4 قصيرة قابلة للعمل دون إنترنت."""
from pathlib import Path
import math, struct, wave, subprocess, shutil
def ensure_media(root):
    root=Path(root); dirs={k:root/k for k in ("images","audio","video")}
    for d in dirs.values(): d.mkdir(parents=True,exist_ok=True)
    for lang in ("ar","en"):
        for level in range(13):
            label="العربية" if lang=="ar" else "English"
            (dirs["images"]/f"{lang}_{level:02d}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720"><rect width="100%" height="100%" fill="white"/><text x="50%" y="45%" text-anchor="middle" font-size="64">{label} — Level {level}</text><text x="50%" y="60%" text-anchor="middle" font-size="34">Lughati offline media</text></svg>',encoding="utf-8")
            wav=dirs["audio"]/f"{lang}_{level:02d}.wav"
            if not wav.exists():
                with wave.open(str(wav),"w") as w:
                    w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
                    for n in range(16000):
                        freq=330+level*20; w.writeframes(struct.pack("<h",int(9000*math.sin(2*math.pi*freq*n/16000))))
            mp4=dirs["video"]/f"{lang}_{level:02d}.mp4"
            if not mp4.exists() and shutil.which("ffmpeg"):
                subprocess.run(["ffmpeg","-y","-f","lavfi","-i","color=c=white:s=640x360:d=1","-c:v","libx264","-pix_fmt","yuv420p",str(mp4)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=False)
    return dirs
