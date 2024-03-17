from __future__ import annotations

NUMBER_OF_QUESTIONS = 10
TEXT_WIDTH = 35
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