import os
import shutil
from datetime import datetime
from dotenv import load_dotenv
load_dotenv(dotenv_path="config/.env" if os.path.exists("config/.env") else ".env")

DATA_PATH = os.getenv("DATA_PATH", "data")
MAX_SESSIONS = int(os.getenv("MAX_SESSIONS", 10))

class StorageManager:
    def __init__(self, data_path=None, max_sessions=None):
        self.data_path = data_path or DATA_PATH
        self.max_sessions = max_sessions or MAX_SESSIONS
        os.makedirs(self.data_path, exist_ok=True)

    def create_new_session(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        session_id = f"session_{ts}"
        path = os.path.join(self.data_path, session_id)
        os.makedirs(path, exist_ok=True)
        print(f"[INFO] Created new session folder: {path}")
        return path

    def cleanup_old_sessions(self):
        sessions = sorted(
            [d for d in os.listdir(self.data_path) if os.path.isdir(os.path.join(self.data_path, d))],
            key=lambda d: os.path.getmtime(os.path.join(self.data_path, d))
        )
        if len(sessions) <= self.max_sessions:
            return
        to_remove = sessions[:-self.max_sessions]
        for s in to_remove:
            p = os.path.join(self.data_path, s)
            try:
                shutil.rmtree(p)
                print(f"[INFO] Deleted old session: {p}")
            except Exception as e:
                print(f"[WARN] Couldn't delete {p}: {e}")

if __name__ == "__main__":
    sm = StorageManager()
    new_session = sm.create_new_session()
    sm.cleanup_old_sessions()
    sm.save_metadata(new_session, {"status": "test run complete"})