from __future__ import annotations

import json
import random
from typing import Any

from const import NUMBER_OF_QUESTIONS, POKEMON_CHOICES

class PMDQuizBackend:

    def __init__(self): 
        self.personality_scores = {}
        self.all_questions = json.load(open("questions.json"))["all_questions"]
        self.all_descriptions = json.load(open("personalities.json"))["all_personalities"]

    def randomize_questions(self):
        return random.sample(self.all_questions, NUMBER_OF_QUESTIONS)
    
    def assign_points(self, chosen_choice: dict[str, Any]) -> None:
        for personality, points in zip(chosen_choice["personalities"], chosen_choice["points"]):
            if personality not in self.personality_scores:
                self.personality_scores[personality] = points
            else:
                self.personality_scores[personality] += points
            
    def get_final_personality(self) -> str:  # TODO: Must check database of pokemon to see which ones are not available anymore
        max_score = max(self.personality_scores.values())
        possible_personalities = [
            personality
            for personality, score in self.personality_scores.items()
            if score == max_score
        ]
        if len(possible_personalities) != 1:
            return random.choice(possible_personalities)
        else:
            return possible_personalities[0]
        
    def get_personality_description(self, personality: str):
        return [
            entry["description"]
            for entry in self.all_descriptions
            if entry["name"] == personality
        ][0]

        
    def get_final_pokemon(self, personality: str) -> str:
        possible_pokemon = POKEMON_CHOICES[personality]  # TODO: Must check database of pokemon to see which ones are not available anymore
        return random.choice(possible_pokemon)
        
