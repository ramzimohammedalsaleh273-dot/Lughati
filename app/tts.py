from pathlib import Path
import platform, subprocess

def speak(text,language="ar"):
    if platform.system()!="Windows": return False
    voice="ar-SA" if language=="ar" else "en-US"
    safe=text.replace("'","''")
    script=f"""Add-Type -AssemblyName System.Speech
$s=New-Object System.Speech.Synthesis.SpeechSynthesizer
try {$s.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::NotSet,[System.Speech.Synthesis.VoiceAge]::NotSet,0,[System.Globalization.CultureInfo]::new("${voice}"))} catch {}
$s.Speak('${safe}')
"""
    subprocess.Popen(["powershell","-NoProfile","-ExecutionPolicy","Bypass","-Command",script],creationflags=subprocess.CREATE_NO_WINDOW)
    return True