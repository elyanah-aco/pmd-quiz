from __future__ import annotations

from datetime import datetime

import json
import pytz
import random
from typing import Any

import pandas as pd

from src.const import DB_FP, MAX_PERSONALITY_ENTRIES, MAX_POKEMON_ENTRIES, NUMBER_OF_QUESTIONS, PERSONALITIES_JSON_FP, POKEMON_CHOICES, QUESTIONS_JSON_FP

class PMDQuizBackend:

    def __init__(self):
        self.results_db = pd.read_csv(DB_FP, index_col=None)
        self.personality_scores = {}
        self.final_personality = None
        self.final_pokemon = None
        
    def randomize_questions(self):
        all_questions = json.load(open(QUESTIONS_JSON_FP))["all_questions"]
        return random.sample(all_questions, NUMBER_OF_QUESTIONS)
    
    def assign_points(self, chosen_choice: dict[str, Any]) -> None:
        for personality, points in zip(chosen_choice["personalities"], chosen_choice["points"]):
            if personality not in self.personality_scores:
                self.personality_scores[personality] = points
            else:
                self.personality_scores[personality] += points
            
    def get_final_personality(self) -> str:
        while not self.final_personality: 
            max_score = max(self.personality_scores.values())
            possible_personalities = [
                personality
                for personality, score in self.personality_scores.items()
                if score == max_score
            ]
            if len(possible_personalities) != 1:
                prelim_personality = random.choice(possible_personalities)
            else:
                prelim_personality = possible_personalities[0]
            
            if prelim_personality not in self.results_db["Personality"].value_counts() or self.results_db["Personality"].value_counts()[prelim_personality] < MAX_PERSONALITY_ENTRIES:
                self.final_personality = prelim_personality
            else:
                del self.personality_scores[prelim_personality]
        
    def get_personality_description(self):
        all_descriptions = json.load(open(PERSONALITIES_JSON_FP))["all_personalities"]
        return [
            entry["description"]
            for entry in all_descriptions
            if entry["name"] == self.final_personality
        ][0]

    def get_final_pokemon(self) -> str:
        possible_pokemon = POKEMON_CHOICES[self.final_personality]
        prelim_pokemon = random.choice(possible_pokemon)
        if prelim_pokemon not in self.results_db["Pokemon"].value_counts() or self.results_db['Pokemon'].value_counts()[prelim_pokemon] < MAX_POKEMON_ENTRIES:
            self.final_pokemon = prelim_pokemon
        else:
            self.final_pokemon = [pokemon for pokemon in possible_pokemon if pokemon != prelim_pokemon][0]

    def update_result_database(self) -> None:
        new_row = pd.DataFrame(
            data=[[self.final_personality, self.final_pokemon, datetime.now(pytz.timezone("Asia/Manila")).strftime("%Y%m%d %H%M%S")]],
            columns=["Personality", "Pokemon", "Result Time"]
            )
        new_row.to_csv(DB_FP, index=False, header=False, mode="a")
        
