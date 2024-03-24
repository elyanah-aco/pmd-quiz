from __future__ import annotations

import time

import pygame
from moviepy.editor import VideoFileClip
from pygame.locals import MOUSEBUTTONDOWN, QUIT

from src.backend import PMDQuizBackend

class PMDQuizApp:
    def __init__(self, video_filename):
        pygame.init()
        self.clip = VideoFileClip(video_filename, audio=False)
        self.window_size = self.clip.size
        self.window = pygame.display.set_mode(self.window_size)
        self.video = self.clip.iter_frames()
        self.frame = next(self.video)  # Get the first frame to start with
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font("assets/PKMN-Mystery-Dungeon.ttf", 36)  # Default font and size

        # Load quiz backend
        self.backend = PMDQuizBackend()
        self.questions = self.backend.randomize_questions()
        self.current_question = 0

    def run(self):
        while self.running and self.current_question < len(self.questions):
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                elif event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    self.check_choice_click(x, y)

            self.play_video_frame()
            if self.current_question < len(self.questions):
                self.display_question(self.questions[self.current_question])
            else:
                self.display_result()
                time.sleep(300)
            pygame.display.update()
            self.clock.tick(self.clip.fps)
        
        pygame.quit()
        sys.exit()

    def play_video_frame(self):
        try:
            self.frame = next(self.video)
        except StopIteration:
            self.video = self.clip.iter_frames()
            self.frame = next(self.video)

        frame_surface = pygame.surfarray.make_surface(self.frame.swapaxes(0, 1))
        self.window.blit(frame_surface, (0, 0))

    def display_question(self, curr_question):
        question = curr_question["question"]
        choices = curr_question["choices"]

        text_surface = self.font.render(question, True, (255, 255, 255))
        self.window.blit(text_surface, (50, 50))

        # Display choices
        y_offset = 100
        for choice in choices:
            choice_text = choice["answer"]
            text_surface = self.font.render(choice_text, True, (255, 255, 255))
            self.window.blit(text_surface, (50, y_offset))
            y_offset += 50

    def check_choice_click(self, x, y):
        curr_question = self.questions[self.current_question]
        choices = curr_question["choices"]
        y_offset = 100
        
        for i, choice in enumerate(choices):
            if 50 <= x <= 50 + self.font.size(choice["answer"])[0] and y_offset <= y <= y_offset + 50:
                self.backend.assign_points(choice)
                print(self.backend.personality_scores)
                self.current_question += 1
                return
            y_offset += 50

    def display_result(self):
        personality = self.backend.get_final_personality()
        result_text = f"Thanks for participating! Your personality is...{personality}!"
        print(result_text)
        text_surface = self.font.render(result_text, True, (255, 255, 255), (0, 0, 0))
        self.window.fill((0, 0, 0))  # Clear the screen
        self.window.blit(text_surface, (50, 50))

if __name__ == "__main__":
    game = PMDQuizApp('assets/background.mp4')  # Replace with your video file path
    game.run()
