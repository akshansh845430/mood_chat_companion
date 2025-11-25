import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
import threading
import subprocess


ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")
AVATAR_MAP = {
    "happy": "avatar_happy.gif",
    "sad": "avatar_sad.gif",
    "angry": "avatar_angry.gif",
    "neutral": "avatar_neutral.gif",
}

# -------------------------------------------------------------------
# Animated GIF Player
# -------------------------------------------------------------------

class GIFLabel(tk.Label):
    def __init__(self, master, gif_path, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.gif_path = gif_path
        self.frames = []
        self.load_frames()

        self.idx = 0
        self.play()

    def load_frames(self):
        gif = Image.open(self.gif_path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.resize((250, 250))  # Avatar size
            self.frames.append(ImageTk.PhotoImage(frame))

    def play(self):
        frame = self.frames[self.idx]
        self.configure(image=frame)
        self.idx = (self.idx + 1) % len(self.frames)
        self.after(80, self.play)  # animation speed


# -------------------------------------------------------------------
# Main UI
# -------------------------------------------------------------------

class MoodCompanionUI:
    def __init__(self, root):

        root.title("Mood Companion")
        root.geometry("420x600")
        root.configure(bg="#101820")

        # Heading
        title = tk.Label(
            root,
            text="Your Mood Companion",
            font=("Helvetica", 20, "bold"),
            bg="#101820",
            fg="#F2AA4C"
        )
        title.pack(pady=10)

        # Avatar container
        self.avatar_box = tk.Frame(root, bg="#101820")
        self.avatar_box.pack(pady=20)

        # Default avatar
        self.avatar_label = GIFLabel(
            self.avatar_box,
            os.path.join(ASSET_DIR, AVATAR_MAP["neutral"])
        )
        self.avatar_label.pack()

        # Text output box
        self.output_text = tk.Text(
            root,
            height=6,
            width=40,
            wrap="word",
            font=("Helvetica", 12),
            bg="#1C1C1C",
            fg="white",
            border=0
        )
        self.output_text.pack(pady=15)

        # Record Button
        record_btn = tk.Button(
            root,
            text="🎙 Speak",
            font=("Helvetica", 16, "bold"),
            bg="#F2AA4C",
            fg="black",
            padx=20,
            pady=10,
            command=self.start_voice_process
        )
        record_btn.pack(pady=30)

    # -------------------------------------------------------------------
    # Trigger backend voice system
    # -------------------------------------------------------------------
    def start_voice_process(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Listening... Speak now.\n")

        def worker():
            # Run your voice companion script
            process = subprocess.Popen(
                ["python", "voice_companion.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.path.dirname(__file__)
            )

            # Read output live
            for line in process.stdout:
                if "Detected Emotion:" in line:
                    emotion = line.split(":")[1].strip().lower()
                    if emotion in AVATAR_MAP:
                        gif_path = os.path.join(ASSET_DIR, AVATAR_MAP[emotion])
                        self.avatar_label = GIFLabel(self.avatar_box, gif_path)
                        self.avatar_label.pack()

                self.output_text.insert(tk.END, line)
                self.output_text.see(tk.END)

        threading.Thread(target=worker).start()


# -------------------------------------------------------------------
# RUN UI
# -------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodCompanionUI(root)
    root.mainloop()
