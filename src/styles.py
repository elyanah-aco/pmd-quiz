from __future__ import annotations

import pyglet
import textwrap
import tkinter as tk

pyglet.font.add_file("assets/PKMN-Mystery-Dungeon.ttf")

import cv2
from PIL import Image, ImageTk

from const import TEXT_WIDTH

class PMDQuizFrontendStyles:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Background App")
        self.root.geometry("800x480")

    def setup_styles(self):
        self.root.configure(background="#f0f0f0")
        self.button_style = {
            "bg": "#204868",
            "fg": "white",
            "font": ("PKMN Mystery Dungeon", 30),
            "padx": 5,
            "pady": 5,
        }
        self.label_style = {
            "bg": "#204868",
            "fg": "white",
            "font": ("PKMN Mystery Dungeon", 45),
            "padx": 15,
            "pady": 15,
            "justify": "left",
        }

    def setup_frames(self):
        self.question_frame = tk.Frame(self.root)
        self.question_frame.place(
            relx=0.5,
            rely=0.8,
            anchor="center",
        )

        self.choices_frame = tk.Frame(self.root, relief=tk.SUNKEN)
        self.choices_frame.place(
            relx=0.9,
            rely=0.4,
            anchor="e",
        )
    
    def wrap_text(self, text: str) -> str:
        return "\n".join(textwrap.wrap(text, width=TEXT_WIDTH))

    def update_video(self):
        # Read a frame from the video
        ret, frame = self.cap.read()

        if ret:
            # Convert frame to RGB format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to Tkinter PhotoImage format
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the video label with the new frame
            self.video_label.config(image=img_tk)
            self.video_label.image = img_tk  # Keep a reference to prevent garbage collection

            # Keep updating the video
            self. root.after(30, self.update_video)
        else:
            self.cap.release() # Release video capture when video ends