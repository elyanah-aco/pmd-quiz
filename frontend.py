import tkinter as tk
from backend import PMDQuizBackend

class PMDQuizFrontend:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Mystery Dungeon - Personality Quiz")
        self.root.geometry("400x300")

        self.backend = PMDQuizBackend()

        self.current_question_index = 0
        self.question_sample = self.backend.randomize_questions()

        self.setup_styles()
        self.display_questions()

    def setup_styles(self):
        self.root.configure(background="#f0f0f0")
        self.button_style = {
            "bg": "#FCAF50",
            "fg": "white",
            "font": ("Arial", 12)
        }

    def display_questions(self):
        if self.current_question_index < len(self.question_sample):
            current_question = self.question_sample[self.current_question_index]
            question, choices = current_question["question"], current_question["choices"]

            self.question_label = tk.Label(
                self.root,
                text=question,
                font=("Arial", 16),
                pady=10
            )
            self.question_label.pack()

            for choice in choices:
                button = tk.Button(
                    self.root,
                    text=choice["answer"],
                    command=lambda c=choice: self.on_button_click(c),
                    **self.button_style
                )
                button.pack()
        else:
            self.display_end_screen()

    def on_button_click(self, chosen_choice):
        self.backend.assign_points(chosen_choice)
        self.current_question_index += 1
        self.clear_widgets()
        self.display_questions()
    
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def display_end_screen(self):
        trait = self.backend.get_final_trait()
        pokemon = self.backend.get_final_pokemon(trait)

        trait_label = tk.Label(
            self.root,
            text=f"Your personality is...{trait}!",
            font=("Arial", 16),
            pady=10
        )
        trait_label.pack()

        pokemon_label = tk.Label(
            self.root,
            text=f"Your Pokemon is...{pokemon}!",
            font=("Arial", 16),
            pady=10
        )
        pokemon_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = PMDQuizFrontend(root)
    root.mainloop()
