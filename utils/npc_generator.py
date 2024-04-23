from typing import TYPE_CHECKING, Dict, Any, Union

from models.npc import Npc
from utils.alignment_tools import random_alignment
from utils.gender_tools import random_gender, pronouns_for
from utils.race_tools import random_race
from utils.name_generator import generate_name
from utils.profession_and_social_class_tools import (
    random_profession,
    random_social_class,
)


def generate_npc(requirements: Dict[str, Any] = {}) -> Union[Npc, None]:
    name_dict = generate_name(requirements)

    requirements["pronouns"] = requirements.get(
        "pronouns", pronouns_for(requirements.get("gender"))
    )

    requirements["social_class"] = requirements.get(
        "social_class", random_social_class()
    )
    requirements["profession"] = requirements.get(
        "profession", random_profession(requirements["social_class"])
    )
    requirements["alignment"] = requirements.get(
        "alignment",
        random_alignment(requirements.get("alignment_requirements", ["N"])),
    )

    if requirements.get("random_profession") == True:
        requirements["profession"] = random_profession(requirements["social_class"])

    return Npc(
        first_name=name_dict["first_name"],
        surname=name_dict["surname"],
        nickname=name_dict["nickname"],
        full_name=name_dict["full_name"],
        gender=name_dict["gender"],
        pronouns=requirements["pronouns"],
        race=name_dict["race"],
        alignment=requirements["alignment"],
        notes={
            "social_class": requirements["social_class"],
            "profession": requirements["profession"],
        },
        campaigns=[1],
    )
