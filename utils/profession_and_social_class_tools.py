from typing import List

from utils.generators import random_from_weight_list

RANDOM_SOCIAL_CLASS_WEIGHTS = {
    "lesser_nobility": 3,
    "religious": 5,
    "academic": 7,
    "military": 8,
    "professional": 20,
    "entertainment": 5,
    "working_class": 47,
    "underclass": 5,
}

RANDOM_PROFESSION_WEIGHTS = {
    "lesser_nobility": {
        "noble": 1,
        "courtier": 3,
        "diplomat": 2,
        "knight": 2,
        "squire": 2,
        "page": 1,
    },
    "religious": {
        "acolyte": 2,
        "priest": 3,
        "druid": 1,
        "monk": 2,
        "paladin": 2,
        "oracle": 1,
    },
    "academic": {
        "arcanist": 8,
        "wizard": 5,
        "healer": 5,
        "scholar": 5,
        "sage": 5,
        "librarian": 2,
        "historian": 2,
        "alchemist": 2,
        "archaeologist": 2,
        "cartographer": 2,
        "herbalist": 2,
        "astrologer": 2,
    },
    "military": {
        "soldier": 25,
        "guard": 5,
        "mercenary": 5,
        "knight": 5,
        "squire": 8,
        "captain": 2,
    },
    "professional": {
        "merchant": 5,
        "artisan": 5,
        "lawyer": 2,
        "doctor": 2,
        "engineer": 2,
        "artificer": 2,
        "armorer": 2,
        "blacksmith": 2,
        "brewer": 2,
        "candlemaker": 2,
        "cartwright": 2,
        "cobbler": 2,
        "cooper": 2,
        "engraver": 2,
        "fletcher": 2,
        "furrier": 2,
        "glassblower": 2,
        "innkeeper": 5,
        "jeweler": 2,
        "leatherworker": 2,
        "locksmith": 2,
        "luthier": 2,
        "potter": 2,
        "saddler": 2,
        "tailor": 2,
        "tanner": 2,
        "tinker": 2,
        "weaponsmith": 2,
        "weaver": 2,
        "woodcarver": 2,
        "potion_maker": 2,
        "scribe": 2,
        "tax_collector": 2,
    },
    "entertainment": {
        "artist": 8,
        "bard": 5,
        "actor": 2,
        "dancer": 2,
        "jester": 2,
    },
    "working_class": {
        "farmer": 25,
        "fisher": 15,
        "miner": 15,
        "herder": 10,
        "trapper": 10,
        "stablehand": 10,
        "shepherd": 5,
        "miller": 5,
        "gamekeeper": 1,
        "vintner": 1,
        "prospector": 1,
        "ditch_digger": 5,
        "stonemason": 5,
        "brickmaker": 5,
        "carpenter": 5,
        "actor": 5,
        "athlete": 5,
        "chef": 1,
        "circus_performer": 5,
        "dancer": 5,
        "poet": 1,
        "writer": 3,
        "sailor": 25,
        "woodcutter": 10,
        "housekeeper": 25,
        "cook": 15,
        "laundry_worker": 5,
    },
    "underclass": {
        "pirate": 1,
        "thief": 2,
        "gangster": 2,
        "brigand": 2,
        "beggar": 2,
        "intern": 2,
        "smuggler": 2,
        "cutpurse": 2,
        "fence": 2,
    },
}


def social_classes() -> List[str]:
    return ["upper_nobility"] + list(RANDOM_SOCIAL_CLASS_WEIGHTS.keys())


def professions() -> List[str]:
    return [
        profession
        for social_class in social_classes()
        for profession in RANDOM_PROFESSION_WEIGHTS[social_class].keys()
    ]


def random_social_class() -> str:
    return random_from_weight_list(RANDOM_SOCIAL_CLASS_WEIGHTS)


def random_profession(social_class: str) -> str:
    return random_from_weight_list(RANDOM_PROFESSION_WEIGHTS[social_class])
