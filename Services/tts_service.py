from gtts import gTTS
import uuid

def text_to_speech(text):
    filename = f"response_{uuid.uuid4().hex}.mp3"
    
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    return filename