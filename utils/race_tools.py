from utils.generators import random_from_weight_list

RANDOM_RACE_WEIGHTS = {
    "human": 50,
    "dwarf": 30,
    "halfling": 30,
    "half-elf": 30,
    "gnome": 20,
    "elf": 20,
    "tiefling": 20,
    "half-orc": 12,
    "goblin": 12,
    "aarakocra": 8,
    "dragonborn": 8,
    "tabaxi": 6,
    "satyr": 4,
    "bugbear": 4,
    "goliath": 2,
    "drow": 2,
    "tortle": 2,
    "air_genasi": 1,
    "earth_genasi": 1,
    "fire_genasi": 1,
    "water_genasi": 1,
}


def random_race() -> str:
    return random_from_weight_list(RANDOM_RACE_WEIGHTS)
