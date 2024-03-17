from __future__ import annotations

import cv2
import tkinter as tk

from backend import PMDQuizBackend
from styles import PMDQuizFrontendStyles

class PMDQuizFrontend(PMDQuizFrontendStyles):
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Mystery Dungeon - Personality Quiz")
        self.root.geometry("800x480")

        self.backend = PMDQuizBackend()

        # Setup video used for background 
        self.cap = cv2.VideoCapture("assets/background.mp4")
        self.video_label = tk.Label(self.root)
        self.video_label.pack(fill="both", expand=True)
        self.update_video()

        # Setup text, frame and button styles
        self.setup_styles()
        self.setup_frames()

        # Run code
        self.current_question_index = 0
        self.question_sample = self.backend.randomize_questions()
        self.determine_personality()
        
    def determine_personality(self):
        if self.current_question_index < len(self.question_sample):
            current_question = self.question_sample[self.current_question_index]
            question, choices = current_question["question"], current_question["choices"]

            self.question_label = tk.Label(
                self.question_frame,
                text=self.wrap_text(question),
                **self.label_style
            )
            self.question_label.pack(side="left")

            for choice in choices:
                button = tk.Button(
                    self.choices_frame,
                    text=choice["answer"],
                    command=lambda c=choice: self.on_choice_button_click(c),
                    **self.button_style
                )
                button.pack(anchor=tk.E, pady=10)
        else:
            personality = self.backend.get_final_personality()
            self.display_personality_screen(personality)

    def on_choice_button_click(self, chosen_choice):
        self.backend.assign_points(chosen_choice)
        self.current_question_index += 1
        self.clear_widgets()
        self.determine_personality()
    
    def clear_widgets(self):
        if hasattr(self, "question_label") and self.question_label:
            self.question_label.destroy()

        for widget in self.choices_frame.winfo_children():
            widget.destroy()
    
    def display_personality_screen(self, personality: str):
        self.clear_widgets()
        
        description = self.backend.get_personality_description(personality)
        self.personality_label = tk.Label(
            self.root,
            text=f"You are the {personality} type!",
            **self.label_style,
        ) 
        self.personality_label.pack()

        self.description_label = tk.Label(
            self.root,
            text=self.wrap_text(description),
            **self.label_style
        )
        self.description_label.pack()
        
        self.next_button = tk.Button(
            self.root,
            text="Next",
            #command=self.display_pokemon_screen(personality)
            **self.button_style
        )
        self.next_button.pack()

    def display_pokemon_screen(self, personality: str):
        self.clear_widgets()

        pokemon = self.backend.get_final_pokemon(personality)
        self.pokemon_label = tk.Label(
            self.root,
            text=f"Your Pokemon is...{pokemon}!",
            font=("Arial", 16),
            pady=10
        )
        self.pokemon_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = PMDQuizFrontend(root)
    root.mainloop()
