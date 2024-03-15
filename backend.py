from __future__ import annotations

import json
import random
from typing import Any

from const import NUMBER_OF_QUESTIONS, POKEMON_CHOICES

class PMDQuizBuilder:

    def __init__(self): 
        self.personality_scores = {}


    def run_game_instance(self):
        all_questions = json.load(open("questions.json"))["all_questions"]
        rand_sample = random.sample(all_questions, NUMBER_OF_QUESTIONS)

        for item in rand_sample:
            question, choices = item["question"], item["choices"]
            self.display_question(question, choices)
            while True:
                user_input = int(input())
                if user_input > len(choices):
                    print("Invalid integer input.")
                else:
                    break
            self.assign_points(choices, user_input)

        trait = self.get_final_trait()
        pokemon = self.get_final_pokemon(trait)
        print(f"Your personality trait is...\n...{trait}!")
        print(f"Your Pokemon is...\n...{pokemon}!")
            
    def display_question(self, question: str, choices: dict[str, Any]) -> None:
        print(question)
        print("\n")
        for ind, choice in enumerate(choices):
            print(f"Choice {ind + 1}: {choice['answer']}")
    
    def assign_points(self, choices: dict[str, Any], user_input: int) -> None:
        chosen_choice = choices[user_input - 1]
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
        possible_pokemon = POKEMON_CHOICES[trait]  # 
        return random.choice(possible_pokemon)

        
