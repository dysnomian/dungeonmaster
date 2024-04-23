"""
Name generator. Generates a random NPC name based on a JSON file of names.
"""

from typing import Union, Dict, Any, List

import json
import os

import random

from utils.gender_tools import random_gender

# Load the names from import_data/names.json
with open(os.path.join(os.path.dirname(__file__), "../import_data/names.json")) as f:
    names = json.load(f)

def select_name(race_name_dict: Dict[str, List], key_name: str, default: Union[str, None]) -> Union[str, None]:
    try:
        if default:
            return default
        else:
            return random.choice(race_name_dict[key_name])
    except KeyError as e:
        print(f"KeyError: {key_name} not found in {key_name}: {e}")


# def generate_name_from_dict(race_name_dict: Dict[str,JDict[str, List]], requirements: Dict[str, Union[str, None]]) -> Dict[str, Union[str, None]]:
#     npc_name_dict = {
#         "first_name": requirements.get("first_name"),
#         "surname": requirements.get("surname"),
#         "full_name": requirements.get("full_name"),
#         "nickname": requirements.get("nickname"),
#         "gender": requirements.get("gender", random_gender()),
#         "race": requirements.get("race")
#     }

#     keys=race_name_dict.keys()

#     # if the species has gendered names, select the appropriate name
#     gendered_names = keys.get("male") else False
#     surnames = True if keys.get("surnames") else False
#     epithets = True if keys.get("epithets") else False
#     nicknames = True if race_name_dict.get("gender_neutral", []).first().matches("(") else False

#     if gendered_names:
#         npc_name_dict["first_name"] = select_name(race_name_dict,







def generate_aarakocra_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "aarakocra",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        name_dict["gender"],
        requirements.get("first_name"))

    name_dict["full_name"] = name_dict["first_name"]

    return name_dict

def generate_bugbear_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "bugbear",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        "gender_neutral",
        requirements.get("first_name"))

    name_dict["full_name"] = name_dict["first_name"]

    name_dict["full_name"] = name_dict["first_name"]

    return name_dict

def generate_dragonborn_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "dragonborn",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        name_dict["gender"],
        requirements.get("first_name"))

    name_dict["surname"] = select_name(
        names[name_dict["race"]],
        "surname",
        requirements.get("surname"))

    name_dict["full_name"] = f"{name_dict["first_name"]} {name_dict["surname"]}"

    return name_dict

def generate_dwarf_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "dwarf",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        name_dict["gender"],
        requirements.get("first_name"))

    name_dict["surname"] = select_name(
        names[name_dict["race"]],
        "surname",
        requirements.get("surname"))

    name_dict["full_name"] = f"{name_dict["first_name"]} {name_dict["surname"]}"

    return name_dict

def generate_elf_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "elf",
        "child": requirements.get("child", False),
        "nickname": None
    }

    gender_key = "child" if name_dict["child"] else name_dict["gender"]

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        gender_key,
        requirements.get("first_name"))

    name_dict["surname"] = select_name(
        names[name_dict["race"]],
        "surname",
        requirements.get("surname"))

    name_dict["full_name"] = f"{name_dict["first_name"]} {name_dict["surname"]}"

    return name_dict

def generate_gnome_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "gnome",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        name_dict["gender"],
        requirements.get("first_name"))

    name_dict["surname"] = select_name(
        names[name_dict["race"]],
        "surname",
        requirements.get("surname"))

    name_dict["full_name"] = f"{name_dict["first_name"]} {name_dict["surname"]}"

    return name_dict

def generate_goblin_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "goblin",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        "gender_neutral",
        requirements.get("first_name"))

    name_dict["full_name"] = name_dict["first_name"]

    name_dict["full_name"] = name_dict["first_name"]

    return name_dict

def generate_goliath_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "goliath",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        name_dict["gender"],
        requirements.get("first_name"))

    name_dict["surname"] = select_name(
        names[name_dict["race"]],
        "surname",
        requirements.get("surname"))

    name_dict["nickname"] = select_name(
        names[name_dict["race"]],
        "epithet",
        requirements.get("nickname"))

    name_dict["full_name"] = f"{name_dict["first_name"]} {name_dict["nickname"]} {name_dict["surname"]}"

    return name_dict


def generate_half_elf_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "half-elf",
        "nickname": None
    }

    elf_name = generate_elf_name(requirements)
    human_name = generate_human_name(requirements)

    name_dict["first_name"] = random.choice([elf_name["first_name"], human_name["first_name"]])

    name_dict["surname"] = random.choice([elf_name["surname"], human_name["surname"]])

    name_dict["full_name"] = f"{name_dict["first_name"]} {name_dict["surname"]}"

    return name_dict

def generate_halfling_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "halfling",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        name_dict["gender"],
        requirements.get("first_name"))

    name_dict["surname"] = select_name(
        names[name_dict["race"]],
        "surname",
        requirements.get("surname"))

    name_dict["full_name"] = f"{name_dict["first_name"]} {name_dict["surname"]}"

    return name_dict

def generate_half_orc_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "half-orc",
        "surname": None,
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        "gender_neutral",
        requirements.get("first_name"))

    name_dict["full_name"] = name_dict["first_name"]

    return name_dict

def generate_tabaxi_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "tabaxi",
        "nickname": None
    }

    name_dict["full_name"] = select_name(
        names[name_dict["race"]],
        "gender_neutral",
        requirements.get("first_name", requirements.get("full_name")))

    # grab the nickname in parentheses
    if name_dict["full_name"].find("(") != -1:
        name_dict["nickname"] = name_dict["full_name"][name_dict["full_name"].find("(")+1:name_dict["full_name"].find(")")]

    # remove the nickname from the full name
    name_dict["full_name"] = name_dict["full_name"].replace(f" ({name_dict['nickname']})", "")

    name_dict["first_name"] = name_dict["nickname"]

    return name_dict

def generate_tiefling_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "tiefling",
        "nickname": None
    }

    # hideous, but half the time, pick a virtue name
    name_dict["first_name"] = random.choice([
        select_name(
        names[name_dict["race"]],
        name_dict["gender"],
        requirements.get("first_name")),
        select_name(
        names[name_dict["race"]],
        "virtue",
        requirements.get("first_name")),
        ])

    name_dict["full_name"] = name_dict["first_name"]

    return name_dict

def generate_tortle_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "tortle",
        "nickname": None
    }

    name_dict["first_name"] = select_name(
        names[name_dict["race"]],
        "gender_neutral",
        requirements.get("first_name"))

    name_dict["full_name"] = name_dict["first_name"]

    return name_dict


def generate_human_name(
    requirements: Dict[str, str] = {},
) -> Dict[str, Union[str, None]]:
    name_dict = {
        "gender": requirements.get("gender", random_gender()),
        "race": "human",
        "nickname": None
    }

    ethnicity = random.choice(
        random.choice(
            [
                ["fantasy"],
                [
                    "arabic",
                    "celtic",
                    "chinese",
                    "egyptian",
                    "english",
                    "french",
                    "german",
                ],
            ]
        )
    )

    name_dict["first_name"] = random.choice(names.get("human").get(ethnicity).get(name_dict["gender"]))
    name_dict["surname"] = random.choice(names.get("human").get("epithets")) + random.choice(names.get("human").get("nouns"))

    name_dict["full_name"] = f"{name_dict["first_name"]} {name_dict["surname"]}"

    return name_dict

def generate_name(requirements: Dict[str, Any] = {}) -> dict:
    # not going to worry about this right now
    child = False

    if requirements.get("race") == "dragonborn":
        return generate_dragonborn_name(requirements)
    elif requirements.get("race") == "dwarf":
        return generate_dwarf_name(requirements)
    elif requirements.get("race") == "elf":
        requirements["child"] = child
        return generate_elf_name(requirements)
    elif requirements.get("race") == "gnome":
        return generate_gnome_name(requirements)
    elif requirements.get("race") == "goliath":
        return generate_goliath_name(requirements)
    elif requirements.get("race") == "goblin":
        return generate_goblin_name(requirements)
    elif requirements.get("race") == "halfling":
        return generate_halfling_name(requirements)
    elif requirements.get("race") == "half-elf":
        return generate_half_elf_name(requirements)
    elif requirements.get("race") == "half-orc":
        return generate_half_orc_name(requirements)
    elif requirements.get("race") == "tabaxi":
        return generate_tabaxi_name(requirements)
    elif requirements.get("race") == "tiefling":
        return generate_tiefling_name(requirements)
    elif requirements.get("race") == "tortle":
        return generate_tortle_name(requirements)
    elif requirements.get("race") == "human":
        return generate_human_name(requirements)
    else:
        return generate_human_name(requirements)
