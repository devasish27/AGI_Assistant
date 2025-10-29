import os
import time
import wave
import threading
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(dotenv_path="config/.env" if os.path.exists("config/.env") else ".env")

import numpy as np
import sounddevice as sd
from mss import mss
import cv2
import tkinter as tk

AUDIO_SAMPLERATE = int(os.getenv("AUDIO_SAMPLERATE", 16000))
SESSION_DURATION = int(os.getenv("SESSION_DURATION", 10))
FPS = int(os.getenv("FPS", 10))

def record_audio_wav(out_path, samplerate=AUDIO_SAMPLERATE, duration=SESSION_DURATION):
    try:
        audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        wf = wave.open(out_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())
        wf.close()
        return True
    except Exception as e:
        print(f"[WARN] Audio recording failed: {e}")
        return False

def record_screen_mp4(out_path, duration=SESSION_DURATION, fps=FPS):
    try:
        with mss() as sct:
            monitor = sct.monitors[1]
            width, height = monitor["width"], monitor["height"]
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
            start = time.time()
            while (time.time() - start) < duration:
                img = sct.grab(monitor)
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
                writer.write(frame)
            writer.release()
        return True
    except Exception as e:
        print(f"[WARN] Screen recording failed: {e}")
        return False

def _mic_window(duration):
    try:
        win = tk.Tk()
        win.overrideredirect(True)
        win.attributes("-topmost", True)
        label = tk.Label(win, text="🎤 Listening...", fg="white", bg="black", font=("Arial", 14, "bold"))
        label.pack(padx=10, pady=8)
        screen_width = win.winfo_screenwidth()
        win.geometry(f"+{screen_width - 260}+60")
        win.after(duration * 1000, win.destroy)
        win.mainloop()
    except Exception as e:
        print(f"[WARN] Mic UI failed: {e}")

def show_mic_symbol(duration=10):
    t = threading.Thread(target=_mic_window, args=(duration,), daemon=True)
    t.start()