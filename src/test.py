import tkinter as tk

class Backend:
    def __init__(self):
        self.questions = []  # Placeholder for questions data

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Multi-Screen App")
        self.geometry("400x300")

        self.backend = Backend()  # Create an instance of the backend class

        # Define label and button styles
        self.label_style = {"font": ("Helvetica", 12)}
        self.button_style = {"font": ("Helvetica", 12), "bg": "lightblue", "fg": "black"}
        self.background_color = "yellow"

        self.current_screen = None

        self.start_screen = StartScreen(self, self.label_style, self.button_style, self.background_color)
        self.question_screen = QuestionScreen(self, self.label_style, self.button_style, self.background_color)
        self.first_result_screen = ResultScreen(self, self.label_style, self.button_style, self.background_color, "First Result Screen")
        self.second_result_screen = ResultScreen(self, self.label_style, self.button_style, self.background_color, "Second Result Screen")

        self.show_start_screen()

    def show_start_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()
        self.start_screen.pack(fill=tk.BOTH, expand=True)
        self.current_screen = self.start_screen

    def show_question_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()
        self.question_screen.pack(fill=tk.BOTH, expand=True)
        self.current_screen = self.question_screen

    def show_first_result_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()
        self.first_result_screen.pack(fill=tk.BOTH, expand=True)
        self.current_screen = self.first_result_screen

    def show_second_result_screen(self):
        if self.current_screen:
            self.current_screen.pack_forget()
        self.second_result_screen.pack(fill=tk.BOTH, expand=True)
        self.current_screen = self.second_result_screen

class StartScreen(tk.Frame):
    def __init__(self, master, label_style, button_style, background_color):
        super().__init__(master)

        self.label_style = label_style  # Reference to the label style
        self.button_style = button_style  # Reference to the button style

        self.configure(bg=background_color)

        tk.Label(self, text="Start Screen", **self.label_style, bg=background_color).pack()

        tk.Button(self, text="Start", command=master.show_question_screen, **self.button_style).pack()

class QuestionScreen(tk.Frame):
    def __init__(self, master, label_style, button_style, background_color):
        super().__init__(master)

        self.label_style = label_style  # Reference to the label style
        self.button_style = button_style  # Reference to the button style

        self.configure(bg=background_color)

        tk.Label(self, text="Question Screen", **self.label_style, bg=background_color).pack()

        tk.Button(self, text="Finish", command=master.show_first_result_screen, **self.button_style).pack()

class ResultScreen(tk.Frame):
    def __init__(self, master, label_style, button_style, background_color, result_text):
        super().__init__(master)

        self.label_style = label_style  # Reference to the label style
        self.button_style = button_style  # Reference to the button style

        self.configure(bg=background_color)

        tk.Label(self, text=result_text, **self.label_style, bg=background_color).pack()

        tk.Button(self, text="Next", command=self.show_next_screen, **self.button_style).pack()

    def show_next_screen(self):
        if self.master.current_screen == self.master.first_result_screen:
            self.master.show_second_result_screen()
        else:
            self.master.show_start_screen()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
