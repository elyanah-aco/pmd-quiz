import textwrap
import tkinter as tk


from backend import PMDQuizBackend
from const import TEXT_WIDTH

class PMDQuizFrontend:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Mystery Dungeon - Personality Quiz")
        self.root.geometry("800x500")

        self.backend = PMDQuizBackend()

        self.current_question_index = 0
        self.question_sample = self.backend.randomize_questions()

        self.setup_styles()
        self.display_questions()

    def setup_styles(self):
        self.root.configure(background="#f0f0f0")
        self.button_style = {
            "bg": "#204868",
            "fg": "white",
            "font": ("Arial", 12)
        }
    
    def wrap_text(self, text: str) -> str:
        return "\n".join(textwrap.wrap(text, width=TEXT_WIDTH))

    def display_questions(self):
        if self.current_question_index < len(self.question_sample):
            current_question = self.question_sample[self.current_question_index]
            question, choices = current_question["question"], current_question["choices"]

            self.question_label = tk.Label(
                self.root,
                text=self.wrap_text(question),
                font=("Arial", 16),
                pady=10
            )
            self.question_label.pack()

            for choice in choices:
                button = tk.Button(
                    self.root,
                    text=choice["answer"],
                    command=lambda c=choice: self.on_choice_button_click(c),
                    **self.button_style
                )
                button.pack()
        else:
            personality = self.backend.get_final_personality()
            self.display_personality_screen(personality)
            self.display_pokemon_screen(personality)


    def on_choice_button_click(self, chosen_choice):
        self.backend.assign_points(chosen_choice)
        self.current_question_index += 1
        self.clear_widgets()
        self.display_questions()
    
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def display_personality_screen(self, personality: str):
        self.clear_widgets()
        
        description = self.backend.get_personality_description(personality)
        self.personality_label = tk.Label(
            self.root,
            text=f"You are the {personality} type!",
            font=("Arial", 16),
            pady=10
        ) 
        self.personality_label.pack()

        self.description_label = tk.Label(
            self.root,
            text=self.wrap_text(description),
            font=("Arial", 12),
            justify="left"
        )
        self.description_label.pack()
        
        self.next_button = tk.Button(
            self.root,
            text="Next",
            command=self.display_pokemon_screen(personality)
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
