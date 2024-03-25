from __future__ import annotations

# Frontend style constants
FONT_PATH = "assets/PKMN-Mystery-Dungeon.ttf"

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 800
ALPHA_LEVEL = 220
TEXT_COLOR = (255, 255, 255)

START_HOLD_WAIT = 2000

QUESTION_FRAME_COLOR = (32, 32, 32)
QUESTION_FRAME_WIDTH = 700
QUESTION_FRAME_HEIGHT = 125
CHOICE_FRAME_COLOR = (54, 59, 63)
CHOICE_XRIGHT_POS = 743


# Backend constants
NUMBER_OF_QUESTIONS = 10
POKEMON_CHOICES: dict[str: list[str]] = {
    "Bold": ["Squirtle", "Turtwig"],
    "Brave": ["Charmander", "Pikachu"],
    "Calm": ["Chikorita", "Cyndaquil"],
    "Docile": ["Charmander", "Bulbasaur"],
    "Hardy": ["Torchic", "Treecko"],
    "Hasty": ["Skitty", "Pikachu"],
    "Impish": ["Piplup", "Chimchar"],
    "Jolly": ["Totodile", "Munchlax"],
    "Lonely": ["Bulbasaur", "Mudkip"],
    "Naive": ["Chimchar", "Skitty"],
    "Quiet": ["Treecko", "Chikorita"],
    "Quirky": ["Squirtle", "Piplup"],
    "Rash": ["Mudkip", "Torchic"],
    "Relaxed": ["Munchlax", "Meowth"],
    "Sassy": ["Meowth", "Totodile"],
    "Timid": ["Cyndaquil", "Turtwig"],
}