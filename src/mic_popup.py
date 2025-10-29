# src/mic_popup.py
import tkinter as tk
import sys

def main():
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    win = tk.Tk()
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.configure(bg="black")

    label = tk.Label(win, text="🎤 Listening...", fg="lime", bg="black", font=("Segoe UI", 18, "bold"))
    label.pack(padx=20, pady=10)

    screen_width = win.winfo_screenwidth()
    win.geometry(f"+{screen_width - 250}+40")

    win.after(duration * 1000, win.destroy)
    win.mainloop()

if __name__ == "__main__":
    main()