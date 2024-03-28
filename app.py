from __future__ import annotations

import sys
import textwrap

import pygame
from moviepy.editor import VideoFileClip
from pygame import mixer
from pygame.locals import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT, SRCALPHA

from src.backend import PMDQuizBackend
from src.const import ALPHA_LEVEL, BG_MUSIC_PATH, BLACK_SCREEN_ALPHA_LEVEL, CHOICE_FRAME_COLOR,CHOICE_XRIGHT_POS, FONT_PATH, QUESTION_FRAME_COLOR, QUESTION_FRAME_HEIGHT, QUESTION_FRAME_WIDTH, START_HOLD_WAIT, TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH

WHITE = (255, 255, 255)

class PMDQuizApp:
    def __init__(self, video_filename):

        pygame.init()

        # Initialize and play music
        mixer.init()
        mixer.music.load(BG_MUSIC_PATH)
        mixer.music.play(-1)
        mixer.music.set_volume(0.6)

        # Initialize and play video as background
        self.clip = VideoFileClip(video_filename, audio=False)
        self.window_size = self.clip.size
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pokemon Mystery Dungeon Personality Quiz")
    
        self.video = self.clip.iter_frames()
        self.frame = next(self.video)  # Get the first frame to start with
        self.clock = pygame.time.Clock()
        self.running = True

        # Load quiz backend
        self.backend = PMDQuizBackend()
        self.questions = self.backend.randomize_questions()
        self.current_question = 0
        self.descriptions = None
        self.current_description = 0

        # Initialize styles
        self.title_font = pygame.font.Font(FONT_PATH, 70)
        self.header_font = pygame.font.Font(FONT_PATH, 45)
        self.subheader_font = pygame.font.Font(FONT_PATH, 40)
        self.subsubheader_font = pygame.font.Font(FONT_PATH, 30)

        # Set initial screen
        self.curr_window = "start"
        
    def run(self):
        # Initialize backend params, calculate backend logic
        click_down_time = None
        
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    click_down_time = pygame.time.get_ticks()

                    if self.curr_window == "questions":
                        if self.current_question < len(self.questions):
                            x, y = pygame.mouse.get_pos()
                            self.check_choice_click(x, y)
                        else:
                            self.backend.get_final_personality()
                            self.generate_result_descriptions()
                            self.curr_window = "desc_results"
                    elif self.curr_window == "desc_results":
                        self.current_question = 0
                        if self.current_description < len(self.descriptions):
                            self.show_current_description_line()
                            self.current_description += 1
                        else:
                            self.backend.get_final_pokemon()
                            self.backend.update_result_database()
                            self.curr_window = "pokemon_results"
                            
                elif event.type == MOUSEBUTTONUP:
                    if self.check_press_and_hold(click_down_time):
                        if self.curr_window == "start":
                            self.curr_window = "questions"
                        if self.curr_window == "pokemon_results":

                            

                            # Reset all results, questions
                            self.curr_window = "start"
                            self.questions = self.backend.randomize_questions()
                            self.current_description = 0
                            self.backend.final_personality = None
                            self.backend.final_pokemon = None
                        click_down_time = None

            # Display frontend widgets
            self.play_video_frame()
                   
            if self.curr_window == "start":
                self.display_start_screen()
            elif self.curr_window == "questions":
                if self.current_question < len(self.questions):
                    self.display_question(self.questions[self.current_question])
            elif self.curr_window == "desc_results":
                self.display_desc_results()
            elif self.curr_window == "pokemon_results":
                self.display_pokemon_results()
                

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

        # Fill black screen with alpha transparency
        bg_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(BLACK_SCREEN_ALPHA_LEVEL)
        self.window.blit(bg_surface, (0, 0))

        # Render text widgets
        title_text = "Pokemon Personality Test"
        subtitle_text = "Inspired from the Pokemon Mystery Dungeon games"
        instructions_text = "Please pay P100 to start!"

        title_surface = self.title_font.render(title_text, True, TEXT_COLOR)
        subtitle_surface = self.header_font.render(subtitle_text, True, TEXT_COLOR)
        instructions_surface = self.header_font.render(instructions_text, True, TEXT_COLOR)
        
        title_rect = title_surface.get_rect(center=(410, 75))
        subtitle_rect = subtitle_surface.get_rect(center=(410, title_rect.height + 80))
        instructions_rect = instructions_surface.get_rect(center=(410, subtitle_rect.height + 300))
        
        self.window.blit(title_surface, title_rect)
        self.window.blit(subtitle_surface, subtitle_rect)
        self.window.blit(instructions_surface, instructions_rect)

    def check_press_and_hold(self, click_down_time) -> bool:
        if click_down_time is None:
            return False
        held_time = pygame.time.get_ticks() - click_down_time
        return held_time >= START_HOLD_WAIT
                      
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
            text_surface = self.subheader_font.render(choice_text, True, TEXT_COLOR)
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
            if CHOICE_XRIGHT_POS - self.subheader_font.size(choice["answer"])[0] <= x <= CHOICE_XRIGHT_POS and y_offset <= y <= y_offset + 30:
                self.backend.assign_points(choice)
                self.current_question += 1
                return
            
            if choice != choices[-1]:
                if len(choices[index + 1]["answer"]) <= 20:
                    y_offset -= 45
                else:
                    y_offset -= 65

    # Result (description) window
    def display_desc_results(self):
        # Fill black screen with alpha transparency
        bg_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(BLACK_SCREEN_ALPHA_LEVEL)
        self.window.blit(bg_surface, (0, 0))

        if self.current_description < len(self.descriptions):
            self.show_current_description_line()

    def generate_result_descriptions(self):
        personality_desc_lines = self.backend.get_personality_description().split("\n")
        init_results_lines = [
            "The results are in!",
            f"You are...the {self.backend.final_personality} type!"
            ]
        final_line = [f"As a {self.backend.final_personality} type, the Pokemon that suits you best is..."]
        self.descriptions = init_results_lines + personality_desc_lines + final_line

    def show_current_description_line(self):
        display_surface = pygame.Surface((QUESTION_FRAME_WIDTH, QUESTION_FRAME_HEIGHT), SRCALPHA)
    
        curr_line = self.descriptions[self.current_description]
        curr_line_surface = self.header_font.render(
            self.wrap_text(curr_line, 25), True, WHITE
            )
        curr_line_rect = curr_line_surface.get_rect(
            center=(QUESTION_FRAME_WIDTH/2, QUESTION_FRAME_HEIGHT/2)
        )

        display_surface.blit(curr_line_surface, curr_line_rect)
        self.window.blit(display_surface, (50, 120))

    # Result (Pokemon) window
    def display_pokemon_results(self):
        # Fill black screen with alpha transparency
        bg_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        bg_surface.fill((0, 0, 0))
        bg_surface.set_alpha(BLACK_SCREEN_ALPHA_LEVEL)
        self.window.blit(bg_surface, (0, 0))

        # Display text widgets
        pokemon_text = f"{self.backend.final_pokemon}!"
        thanks_text = "Thanks for playing!"
        claim_text = f"Please claim your {self.backend.final_pokemon} pin and sticker."
        press_text = "Press and hold to return to the start screen"

        pokemon_surface = self.title_font.render(pokemon_text, True, WHITE)
        thanks_surface = self.header_font.render(thanks_text, True, WHITE)
        claim_surface = self.header_font.render(claim_text, True, WHITE)
        press_surface = self.subsubheader_font.render(press_text, True, WHITE)

        pokemon_rect = pokemon_surface.get_rect(center=(410, 75))
        thanks_rect = thanks_surface.get_rect(center=(410, 250))
        claim_rect = claim_surface.get_rect(center=(410, thanks_rect.height + 250))
        press_rect = press_surface.get_rect(center=(410, claim_rect.height + 320))

        self.window.blit(pokemon_surface, pokemon_rect)
        self.window.blit(thanks_surface, thanks_rect)
        self.window.blit(claim_surface, claim_rect)
        self.window.blit(press_surface, press_rect)

if __name__ == "__main__":
    game = PMDQuizApp('assets/background.mp4')  # Replace with your video file path
    game.run()
