from __future__ import annotations

import sys
import textwrap

import pygame
from moviepy.editor import VideoFileClip
from pygame.locals import MOUSEBUTTONDOWN, QUIT

from src.backend import PMDQuizBackend
from src.const import ALPHA_LEVEL, CHOICE_FRAME_COLOR,CHOICE_XRIGHT_POS, FONT_PATH, QUESTION_FRAME_COLOR, QUESTION_FRAME_HEIGHT, QUESTION_FRAME_WIDTH, TEXT_COLOR

class PMDQuizApp:
    def __init__(self, video_filename):
        pygame.init()
        self.clip = VideoFileClip(video_filename, audio=False)
        self.window_size = self.clip.size
        self.window = pygame.display.set_mode((800, 400))
        self.video = self.clip.iter_frames()
        self.frame = next(self.video)  # Get the first frame to start with
        self.clock = pygame.time.Clock()
        self.running = True

        # Load quiz backend
        self.backend = PMDQuizBackend()
        self.questions = self.backend.randomize_questions()
        self.current_question = 0
        self.personality = None

        # Initialize styles
        self.title_font = pygame.font.Font(FONT_PATH, 70)
        self.header_font = pygame.font.Font(FONT_PATH, 45)
        self.subheader_font = pygame.font.Font(FONT_PATH, 40)

        # Set initial screen
        self.curr_window = "start"
        

    def run(self):

        # Initialize/calculate backend params
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if self.curr_window == "questions":
                        if self.current_question < len(self.questions):
                            x, y = pygame.mouse.get_pos()
                            self.check_choice_click(x, y)
                        else:
                            self.backend.get_final_personality()
                            self.curr_window = "results"
                    elif self.curr_window == "results":
                        self.current_question = 0    

            # Display frontend widgets
            self.play_video_frame()
                  
            if self.curr_window == "start":
                self.display_start_screen()
            elif self.curr_window == "questions":
                if self.current_question < len(self.questions):
                    self.display_question(self.questions[self.current_question])
            elif self.curr_window == "results":
                self.display_results()

            pygame.display.update()
            self.clock.tick(self.clip.fps)

        pygame.quit()
        sys.exit()

    def wrap_text(self, text: str, chars_per_line: int) -> str:
        return "\n".join(textwrap.wrap(text, width=chars_per_line))
        
    def play_video_frame(self):
        try:
            self.frame = next(self.video)
        except StopIteration:
            self.video = self.clip.iter_frames()
            self.frame = next(self.video)

        frame_surface = pygame.surfarray.make_surface(self.frame.swapaxes(0, 1))
        self.window.blit(frame_surface, (0, 0))

    def display_start_screen(self):
        title_text = "Pokemon Personality Test!"
        title_surface = self.title_font.render(title_text, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(
            center=(410, 75)
        )
        self.window.blit(title_surface, title_rect)

        start_button_rect = pygame.Rect(360, 200, 200, 100)
        pygame.draw.rect(self.window, (0, 255, 0), start_button_rect, 2)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    self.curr_window = "questions"

    def display_question(self, curr_question):
        question = self.wrap_text(curr_question["question"], 40)
        choices = curr_question["choices"]

        # Add question frame
        question_surface = pygame.Surface((QUESTION_FRAME_WIDTH, QUESTION_FRAME_HEIGHT))
        question_surface.set_alpha(ALPHA_LEVEL)
        question_surface.fill(QUESTION_FRAME_COLOR)
    
        # Render question text in frame
        question_text_surface = self.header_font.render(
            question, True, TEXT_COLOR
            )
        question_text_rect = question_text_surface.get_rect(
            center=(QUESTION_FRAME_WIDTH/2, QUESTION_FRAME_HEIGHT/2)
        )
    
        question_surface.blit(question_text_surface, question_text_rect)
        self.window.blit(question_surface, (50, 240))
        
        # Display choices
        y_offset = 180
        for index, choice in enumerate(choices):
            choice_text = self.wrap_text(choice["answer"], 20)
            text_surface = self.subheader_font.render(choice_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.topright = (CHOICE_XRIGHT_POS, y_offset)
            
            pygame.draw.rect(
                self.window,
                CHOICE_FRAME_COLOR,
                (text_rect.left - 5, text_rect.top - 5, text_rect.width + 12, text_rect.height + 12)
            )

            self.window.blit(text_surface, text_rect)
            if choice != choices[-1]:
                if len(choices[index + 1]["answer"]) <= 20:
                    y_offset -= 45
                else:
                    y_offset -= 65

    def check_choice_click(self, x, y):
        curr_question = self.questions[self.current_question]
        choices = curr_question["choices"]
        y_offset = 180
        
        for index, choice in enumerate(choices):
            if CHOICE_XRIGHT_POS- self.subheader_font.size(choice["answer"])[0] <= x <= CHOICE_XRIGHT_POS and y_offset <= y <= y_offset + 30:
                self.backend.assign_points(choice)
                self.current_question += 1
                return
            
            if choice != choices[-1]:
                if len(choices[index + 1]["answer"]) <= 20:
                    y_offset -= 45
                else:
                    y_offset -= 65

    def display_results(self):   
        result_text = f"Thanks for participating! Your personality is...{self.backend.final_personality}!"
        text_surface = self.header_font.render(result_text, True, (255, 255, 255))
        self.window.blit(text_surface, (50, 50))

if __name__ == "__main__":
    game = PMDQuizApp('assets/background.mp4')  # Replace with your video file path
    game.run()
