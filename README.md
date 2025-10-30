## 📘 **README.md**


# 🤖AGI Assistant: Voice-Controlled Intelligent Desktop Automation System

## 🧩 Overview
**AGI Assistant** is an intelligent desktop automation tool that:
- Listens to your **voice commands**
- Records both **audio** and **screen activity**
- Performs **context-aware automation** such as opening Excel, File Explorer, Browser, or WhatsApp
- Generates a detailed **session summary (JSON)** describing the detected actions and extracted screen text

This project combines **speech recognition**, **OCR**, and **desktop automation** into one integrated workflow.

---

## ⚙️ Features
✅ Voice-based automation using the **Vosk offline speech model**  
✅ Screen OCR analysis with **Tesseract**  
✅ Automatic generation of session logs in `/data/`  
✅ Action detection — “open excel”, “open browser”, “open whatsapp”  
✅ Fallback automation when no valid audio detected  
✅ Cross-compatible — works both as `.py` and `.exe`

---

## 🧠 Project Workflow
1. Launches mic popup and records audio for a fixed duration (default: 10s)
2. Captures a screen video in parallel
3. Transcribes the audio → detects intent (Excel, File Explorer, Browser, etc.)
4. Performs the matching action automatically
5. Extracts text from captured frames using Tesseract OCR
6. Saves results inside a new `data/session_YYYYMMDD_HHMMSS/` folder

---

## 🧩 Project Structure


AGI_Assistant1/

├── src/
│   ├── main.py                # Main entry point

│   ├── summarizer.py          # Speech + OCR summarization

│   ├── automation_manager.py  # Executes detected automation

│   ├── storage_manager.py     # Handles data/session management

│   ├── recorder.py            # Audio & screen recording

│   └── ...

│

├── models/

│   └── vosk_model/            # Vosk speech recognition model files

│
├── config/

│   └── .env                   # Optional configuration (paths, duration, etc.)

│

├── data/                      # Saved session recordings and summaries

│   └── session_YYYYMMDD_HHMMSS/
│

├── requirements.txt

├── README.md

└── AGI_Assistant.exe          # (Optional) Built executable



---

## 🪄 Installation

### 1️⃣ Clone or extract the project
```bash
cd C:\Users\<YourName>\PycharmProjects\AGI_Assistant1
````

### 2️⃣ Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Place Vosk Model

Download a lightweight English model from:
🔗 [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)

Extract it inside:

```
models\vosk_model\
```

### 5️⃣ Install Tesseract OCR

Install from:
🔗 [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Then ensure the path is correct in `main.py` or `.env`:

```
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

---

## ▶️ Usage

### 🧩 Run via Python

```bash
venv\Scripts\activate
python src\main.py
```

### 🧩 Run as Executable

After packaging with PyInstaller (see below), run:

```bash
cd dist
AGI_Assistant.exe
```

The mic symbol will appear briefly, then the app will:

* Record voice and screen
* Detect commands like:

  * “open excel”
  * “open browser”
  * “open whatsapp”
  * “open files” (fallback)

Results will appear in `/data/session_.../summary.json`.

---

## 🏗️ Building Executable (.exe)

### Run this in **CMD** (not PowerShell)

```cmd
cd C:\Users\<YourName>\PycharmProjects\AGI_Assistant1
venv\Scripts\activate
python -m PyInstaller --onefile --noconsole ^
--name "AGI_Assistant" ^
--add-data "models;models" ^
--add-data "config;config" ^
--add-data "data;data" ^
src\main.py
```

The output `.exe` will be located in:

```
dist\AGI_Assistant.exe
```

---

## 🧾 Output Example

**summary.json**

```json
{
    "timestamp": "20251028_121755",
    "audio_text": "open excel",
    "screen_text_samples": ["Microsoft Excel - Book1"],
    "detected_actions": [
        {"action": "Opened Excel", "source": "audio"},
        {"action": "Interacted with screen", "source": "ocr"}
    ],
    "final_action": "Opened Excel"
}
```

---

## 🧹 Logs & Cleanup

Old sessions are automatically cleaned when more than 10 exist (configurable in `.env`):

```
MAX_SESSIONS=10
```

---

## 🧩 Troubleshooting

| Issue                       | Fix                                                                 |
| --------------------------- | ------------------------------------------------------------------- |
| ❌ “explorer not recognized” | Add `C:\Windows\explorer.exe` to PATH or use `os.startfile("C:\\")` |
| 🎙️ Mic not recording       | Ensure audio permissions or update `pyaudio`                        |
| 🧠 No speech detected       | Check if vosk model folder exists                                   |
| ⚙️ OCR not extracting text  | Confirm `TESSERACT_PATH` is valid                                   |
| 💥 .exe doesn’t run         | Always rebuild after activating venv                                |

---

## 👨‍💻 Author

**Devasish Pothumudi**
AI/ML Engineer | Automation & Speech Systems Developer

---

## 📜 License

MIT License © 2025 Devasish Pothumudi

---
