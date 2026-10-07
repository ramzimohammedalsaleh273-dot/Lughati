import platform, subprocess

def speak(text,language="ar"):
    if platform.system()!="Windows": return False
    voice="ar-SA" if language=="ar" else "en-US"
    safe=text.replace("'","''")
    script=("Add-Type -AssemblyName System.Speech\n"
             "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer\n"
             "try {$s.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::NotSet,[System.Speech.Synthesis.VoiceAge]::NotSet,0,[System.Globalization.CultureInfo]::new(\"" + voice + "\") )} catch {}\n"
             "$s.Speak('" + safe + "')\n")
    subprocess.Popen(["powershell","-NoProfile","-ExecutionPolicy","Bypass","-Command",script],creationflags=subprocess.CREATE_NO_WINDOW)
    return True