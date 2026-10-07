from pathlib import Path

AUDIO_EXTENSIONS={".mp3",".wav",".ogg",".m4a",".aac",".flac"}
VIDEO_EXTENSIONS={".mp4",".webm",".mkv",".avi",".mov",".m4v"}

def scan_media(root: Path):
    root=Path(root)
    audio=[]; video=[]
    if not root.exists(): return audio,video
    for p in sorted(root.rglob("*")):
        if not p.is_file(): continue
        if p.suffix.lower() in AUDIO_EXTENSIONS: audio.append(p)
        elif p.suffix.lower() in VIDEO_EXTENSIONS: video.append(p)
    return audio,video
