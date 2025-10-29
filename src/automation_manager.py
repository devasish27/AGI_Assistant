import os
import json
import time
import logging
import subprocess
import platform

# ------------------------------------------------------------------
# Automation Manager
# ------------------------------------------------------------------

class AutomationManager:
    def __init__(self):
        """Handles performing system-level actions based on summarized user input."""
        self.action_map = {
            "Opened Excel": self.open_excel,
            "Opened File Explorer": self.open_file_explorer,
            "Opened Browser": self.open_browser,
            "Opened WhatsApp": self.open_whatsapp,
            "Saved file": self.save_file_sim,
            "Fallback: Opened File Explorer": self.open_file_explorer
        }

    # ------------------------------------------------------------------
    def open_excel(self):
        """Launch Excel safely."""
        try:
            logging.info("📂 Opening Excel...")
            if platform.system() == "Windows":
                subprocess.Popen(["cmd", "/c", "start", "excel"], shell=True)
            else:
                subprocess.Popen(["libreoffice", "--calc"])
        except Exception as e:
            logging.error(f"Failed to open Excel: {e}")
            self.open_file_explorer()
    # ------------------------------------------------------------------
    def open_file_explorer(self):
        """Open system File Explorer."""
        try:
            logging.info("🗂️ Opening File Explorer...")
            if platform.system() == "Windows":
                subprocess.Popen(["cmd", "/c", "start", "."], shell=True)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "."])
            else:
                subprocess.Popen(["xdg-open", "."])
        except Exception as e:
            logging.error(f"Could not open File Explorer: {e}")
    # ------------------------------------------------------------------
    def open_browser(self):
        try:
            logging.info("🌐 Opening Browser (default)...")
            if platform.system() == "Windows":
                subprocess.Popen("start chrome", shell=True)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-a", "Google Chrome"])
            else:
                subprocess.Popen(["xdg-open", "https://www.google.com"])
        except Exception as e:
            logging.error(f"❌ Browser launch failed: {e}")

    # ------------------------------------------------------------------
    def open_whatsapp(self):
        try:
            logging.info("💬 Opening WhatsApp...")
            if platform.system() == "Windows":
                # Launch WhatsApp Desktop if installed
                subprocess.Popen("start whatsapp", shell=True)
            else:
                subprocess.Popen(["xdg-open", "https://web.whatsapp.com"])
        except Exception as e:
            logging.error(f"❌ WhatsApp launch failed: {e}")

    # ------------------------------------------------------------------
    def save_file_sim(self):
        logging.info("💾 Simulating file save action (placeholder).")

    # ------------------------------------------------------------------
    def unknown_action(self):
        """Fallback action for unknown or invalid commands."""
        logging.warning("⚠️ Unknown action encountered. Opening File Explorer as fallback.")
        self.open_file_explorer()

    # ------------------------------------------------------------------
    def execute_latest(self, session_path):
        """Reads the latest summary.json and performs the detected final action."""
        summary_path = os.path.join(session_path, "summary.json")
        if not os.path.exists(summary_path):
            logging.error(f"❌ No summary.json found at {summary_path}")
            return

        with open(summary_path, "r", encoding="utf-8") as f:
            summary = json.load(f)

        detected_actions = summary.get("detected_actions", [])
        final_action = summary.get("final_action")

        # ✅ Prefer the first audio-sourced action if available
        preferred_action = None
        for a in detected_actions:
            if isinstance(a, dict) and a.get("source") == "audio":
                preferred_action = a.get("action")
                break

        # fallback to final_action if audio not available
        chosen_action = preferred_action or final_action or "Fallback: Opened File Explorer"

        logging.info(f"🚀 Final action chosen: {chosen_action}")

        # Execute the mapped action
        action_func = self.action_map.get(chosen_action, self.unknown_action)
        action_func()

        # Log completion
        logging.info("✅ Action executed successfully.")
        time.sleep(1)