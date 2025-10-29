#summarizer.py
import os, sys, json, wave
from datetime import datetime
from difflib import SequenceMatcher
import cv2, pytesseract

try:
    from vosk import Model, KaldiRecognizer
except Exception:
    Model = None
    KaldiRecognizer = None

if getattr(sys, "frozen", False):
    os.environ["PATH"] = sys._MEIPASS + os.pathsep + os.environ.get("PATH", "")

if os.path.exists(r"C:\Program Files\Tesseract-OCR\tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class Summarizer:
    def __init__(self, vosk_model_path="models/vosk_model"):
        if Model and os.path.exists(vosk_model_path):
            try:
                self.asr_model = Model(vosk_model_path)
                print("[INFO] Vosk model loaded.")
            except Exception as e:
                print(f"[WARN] Could not load Vosk model: {e}")
                self.asr_model = None
        else:
            print("[WARN] Vosk model unavailable.")
            self.asr_model = None

    def transcribe_audio(self, audio_path):
        if not self.asr_model or not os.path.exists(audio_path):
            return ""
        try:
            wf = wave.open(audio_path, "rb")
            rec = KaldiRecognizer(self.asr_model, wf.getframerate())
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    results.append(json.loads(rec.Result()))
            results.append(json.loads(rec.FinalResult()))
            text = " ".join([r.get("text", "") for r in results])
            wf.close()
            return text.strip()
        except Exception as e:
            print(f"[WARN] Transcription failed: {e}")
            return ""

    def extract_screens_text(self, video_path, frame_skip=60):
        if not os.path.exists(video_path):
            return []
        cap = cv2.VideoCapture(video_path)
        frames_text = []
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if count % frame_skip == 0:
                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    text = pytesseract.image_to_string(gray)
                    if text.strip():
                        frames_text.append(text.strip())
                except Exception:
                    pass
            count += 1
        cap.release()
        return frames_text

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def detect_actions(self, audio_text, screen_texts):
        actions = []
        audio_lower = (audio_text or "").lower()
        keywords = {
            "excel": ["excel", "xl", "axel"],
            "save": ["save", "safe"],
            "file": ["file", "explorer", "open file"],
            "browser": ["browser", "chrome", "edge"],
            "whatsapp": ["whatsapp", "what'sapp"]
        }
        def matches_any(word_list):
            return any(self.similar(k, w) > 0.6 for k in word_list for w in audio_lower.split())

        if matches_any(keywords["excel"]): actions.append({"action": "Opened Excel", "source": "audio"})
        if matches_any(keywords["save"]): actions.append({"action": "Saved file", "source": "audio"})
        if matches_any(keywords["file"]): actions.append({"action": "Opened File Explorer", "source": "audio"})
        if matches_any(keywords["browser"]): actions.append({"action": "Opened Browser", "source": "audio"})
        if matches_any(keywords["whatsapp"]): actions.append({"action": "Opened WhatsApp", "source": "audio"})
        if screen_texts: actions.append({"action": "Interacted with screen", "source": "ocr"})
        if not actions:
            actions.append({"action": "Fallback: Opened File Explorer", "source": "fallback"})
        return actions

    def generate_summary_files(self, session_path, actions, audio_text, screen_texts):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        data = {
            "timestamp": ts,
            "audio_text": audio_text,
            "screen_text_samples": screen_texts[:5],
            "detected_actions": actions,
            "final_action": actions[-1]["action"] if actions else "Fallback"
        }
        with open(os.path.join(session_path, "summary.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[INFO] Summary saved for {session_path}")
        return data

    def process_session(self, session_path):
        audio_path = os.path.join(session_path, "audio.wav")
        video_path = os.path.join(session_path, "screen.mp4")
        audio_text = self.transcribe_audio(audio_path)
        screen_texts = self.extract_screens_text(video_path)
        actions = self.detect_actions(audio_text, screen_texts)
        return self.generate_summary_files(session_path, actions, audio_text, screen_texts)