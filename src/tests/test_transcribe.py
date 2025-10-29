import os
import logging
from vosk import Model, KaldiRecognizer
import wave
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

MODEL_PATH = "models/vosk_model"
DATA_PATH = "data"

def get_latest_session():
    sessions = [s for s in os.listdir(DATA_PATH) if s.startswith("session_")]
    if not sessions:
        return None
    sessions.sort(reverse=True)
    return os.path.join(DATA_PATH, sessions[0])

def transcribe_audio(audio_path):
    if not os.path.exists(audio_path):
        logging.warning(f"Audio file missing: {audio_path}")
        return ""

    logging.info("Vosk model loaded.")
    wf = wave.open(audio_path, "rb")
    model = Model(MODEL_PATH)
    rec = KaldiRecognizer(model, wf.getframerate())
    
    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text += " " + result.get("text", "")
    wf.close()
    return text.strip()

if __name__ == "__main__":
    session_path = get_latest_session()
    if not session_path:
        logging.error("No sessions found in data/. Run main.py first.")
    else:
        audio_path = os.path.join(session_path, "audio.wav")
        result = transcribe_audio(audio_path)
        print(f"🗣️ Transcribed text: {result if result else '[no speech detected]'}")