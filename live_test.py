import sounddevice as sd
import scipy.io.wavfile as wav
import uuid

from Backend.Services.stt_service import transcribe_audio
from Backend.Services.rag_service import get_context
from Backend.Services.llm_service import generate_response
from Backend.Services.tts_service import text_to_speech

# 🎤 Record audio
def record_audio(filename, duration=5, fs=16000):
    print("🎤 Speak now...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav.write(filename, fs, recording)
    print("✅ Recording done")

def run():
    filename = f"input_{uuid.uuid4().hex}.wav"

    # Step 1: Record
    record_audio(filename)

    # Step 2: STT
    text = transcribe_audio(filename)
    print("📝 You:", text)

    # Step 3: RAG
    context = get_context(text)

    # Step 4: LLM
    response = generate_response(text, context)
    print("🤖 Bot:", response)

    # Step 5: TTS
    audio_file = text_to_speech(response)

    # Step 6: Play audio
    import os
    os.system(f"start {audio_file}")  # Windows

if __name__ == "__main__":
    run()