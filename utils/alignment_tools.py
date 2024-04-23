import random

from typing import List


def alignment_options(requirements: List[str] = ["A"]) -> List[str]:
    if "A" in requirements:
        return ["LG", "NG", "CG", "LN", "N", "CN", "LE", "NE", "CE"]
    elif "G" in requirements:
        return ["LG", "NG", "CG"]
    elif "E" in requirements:
        return ["LE", "NE", "CE"]
    elif "L" in requirements:
        return ["LG", "LN", "LE"]
    elif "C" in requirements:
        return ["CG", "CN", "CE"]
    else:
        return requirements


def random_alignment(requirements: List[str] = ["A"]) -> str:
    return random.choice(alignment_options(requirements))
