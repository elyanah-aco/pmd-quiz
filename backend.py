from __future__ import annotations

import json
import random
from typing import Any

from const import NUMBER_OF_QUESTIONS, POKEMON_CHOICES

class PMDQuizBackend:

    def __init__(self): 
        self.personality_scores = {}

    def randomize_questions(self):
        all_questions = json.load(open("questions.json"))["all_questions"]
        rand_sample = random.sample(all_questions, NUMBER_OF_QUESTIONS)
        return rand_sample
    
    def assign_points(self, chosen_choice: dict[str, Any]) -> None:
        for trait, points in zip(chosen_choice["traits"], chosen_choice["points"]):
            if trait not in self.personality_scores:
                self.personality_scores[trait] = points
            else:
                self.personality_scores[trait] += points
            
    def get_final_trait(self) -> str:  # TODO: Must check database of pokemon to see which ones are not available anymore
        max_score = max(self.personality_scores.values())
        possible_traits = [
            trait
            for trait, score in self.personality_scores.items()
            if score == max_score
        ]
        if len(possible_traits) != 1:
            return random.choice(possible_traits)
        else:
            return possible_traits[0]
        
    def get_final_pokemon(self, trait: str) -> str:
        possible_pokemon = POKEMON_CHOICES[trait]  # TODO: Must check database of pokemon to see which ones are not available anymore
        return random.choice(possible_pokemon)

    def test_button_click(self):
        return 1
        
