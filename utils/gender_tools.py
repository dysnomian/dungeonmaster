from utils.generators import random_from_weight_list


RANDOM_GENDER_WEIGHTS = {"male": 45, "female": 45, "non-binary": 10}


def random_gender() -> str:
    return random_from_weight_list(RANDOM_GENDER_WEIGHTS)


def pronouns_for(gender) -> str:
    if gender == "male":
        return "he/him"
    elif gender == "female":
        return "she/her"
    else:
        return "they/them"
