import os, sys, threading, time
from dotenv import load_dotenv
from storage_manager import StorageManager
from recorder import record_audio_wav, record_screen_mp4, show_mic_symbol
from summarizer import Summarizer
from automation_manager import AutomationManager

# If frozen (PyInstaller exe), make project root the parent of dist/
if getattr(sys, "frozen", False):
    exe_dir = os.path.dirname(sys.executable)
    project_root = os.path.dirname(exe_dir)
    os.chdir(os.path.dirname(sys.executable))
    os.environ["PATH"] = sys._MEIPASS + os.pathsep + os.environ.get("PATH", "")

load_dotenv(dotenv_path="config/.env" if os.path.exists("config/.env") else ".env")

SESSION_DURATION = int(os.getenv("SESSION_DURATION", 10))
AUDIO_SAMPLERATE = int(os.getenv("AUDIO_SAMPLERATE", 16000))
FPS = int(os.getenv("FPS", 10))
DATA_PATH = os.getenv("DATA_PATH", "data")
MAX_SESSIONS = int(os.getenv("MAX_SESSIONS", 10))
VOSK_MODEL_PATH = os.getenv("VOSK_MODEL_PATH", "models/vosk_model")
TESSERACT_PATH = os.getenv("TESSERACT_PATH")

try:
    import pytesseract
    if TESSERACT_PATH and os.path.exists(TESSERACT_PATH):
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
except Exception:
    pytesseract = None

# -----Main logic --------
def process_and_analyze(session_path, _ ):
    """Generate summary and run automation."""
    summarizer = Summarizer(vosk_model_path=VOSK_MODEL_PATH)
    summary = summarizer.process_session(session_path)
    print(f"[INFO] Summary JSON generated at: {os.path.join(session_path, 'summary.json')}")
    print(f"[INFO] Detected actions: {summary.get('detected_actions', [])}")
    automation = AutomationManager()
    automation.execute_latest(session_path)


def main():
    print("[INFO] === AGI Assistant Started ===")
    storage = StorageManager(data_path=DATA_PATH, max_sessions=MAX_SESSIONS)
    storage.cleanup_old_sessions()
    session_path = storage.create_new_session()

    audio_path = os.path.join(session_path, "audio.wav")
    screen_path = os.path.join(session_path, "screen.mp4")

    mic_thread = threading.Thread(target=show_mic_symbol, args=(SESSION_DURATION,), daemon=True)
    mic_thread.start()

    record_audio_wav(audio_path, samplerate=AUDIO_SAMPLERATE, duration=SESSION_DURATION)
    record_screen_mp4(screen_path, duration=SESSION_DURATION, fps=FPS)

    print(f"[INFO] Audio saved: {audio_path}")
    print(f"[INFO] Screen saved: {screen_path}")

    try:
        process_and_analyze(session_path, DATA_PATH)
    except Exception as e:
        print(f"[ERROR] Analysis failed: {e}")

    print(f"[INFO] Completed session: {session_path}")
    print("[INFO] Exiting in 3s...")
    time.sleep(3)


if __name__ == "__main__":
    main()