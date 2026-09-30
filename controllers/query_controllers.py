import uuid
from Backend.Services.stt_service import transcribe_audio
from Backend.Services.rag_service import get_context
from Backend.Services.llm_service import generate_response
from Backend.Services.tts_service import text_to_speech

async def process_query(file):
    file_path = f"temp_{uuid.uuid4().hex}.wav"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 🎤 STT
    query = transcribe_audio(file_path)

    # 📚 RAG
    context = get_context(query)

    # 🤖 LLM
    response = generate_response(query, context)

    # 🔊 TTS
    audio_file = text_to_speech(response)

    return {
        "query": query,
        "response": response,
        "audio": f"http://localhost:8000/audio/{audio_file}"
    }