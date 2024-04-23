import random

from typing import Dict


def random_from_weight_list(weight_list: Dict[str, int]) -> str:
    return random.choices(list(weight_list.keys()), weights=list(weight_list.values()))[
        0
    ]
