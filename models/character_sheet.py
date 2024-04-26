import json

from typing import List, Dict, Any, Annotated, TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from utils.logging import logger
from models.base import Base
from models.campaign_pcs_table import campaign_pcs_table

if TYPE_CHECKING:
    from models.player import Player
    from models.campaign import Campaign
else:
    Player = "Player"
    Campaign = "Campaign"


default_classes = [
    {
        "name": "Fighter",
        "level": 1,
        "features": [
            {
                "name": "Protection",
                "type": "Fighting Style",
                "description": "When a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to impose disadvantage on the attack roll. You must be wielding a shield.",
            },
            {
                "name": "Second Wind",
                "type": "Class Feature",
                "description": "On your turn, you can use a bonus action to regain 1d10 + 1 hit points. Once you use this feature, you must finish a short or long rest before you can use it again.",
            },
        ],
    }
]
default_background = {
    "name": "Soldier",
    "selections": {
        "proficiencies": {"skills": ["Investigation"], "tools": ["Dice Set"]}
    },
}
default_level_up_system = {
    "type": "Experience Points",
    "current_xp": 0,
    "next_level_xp": 300,
}


def feat_names() -> List[str]:
    feat_names = []

    with open("feats.json", "r") as f:
        feats = json.load(f)

    for feat in feats:
        feat_names.append(feat["name"])
    return feat_names

    # parse feats into a dict with the structure


def default_ability_scores(character_class: str) -> Dict[str, int]:
    scores_dict = {
        # "artificer": {
        #     "STR": 8,
        #     "DEX": 14,
        #     "CON": 14,
        #     "INT": 15,
        #     "WIS": 10,
        #     "CHA": 10,
        # },
        "barbarian": {
            "STR": 15,
            "DEX": 14,
            "CON": 14,
            "INT": 8,
            "WIS": 10,
            "CHA": 10,
        },
        # "bard": {
        #     "STR": 8,
        #     "DEX": 15,
        #     "CON": 14,
        #     "INT": 8,
        #     "WIS": 10,
        #     "CHA": 15,
        # },
        # "cleric": {
        #     "STR": 15,
        #     "DEX": 8,
        #     "CON": 14,
        #     "INT": 8,
        #     "WIS": 15,
        #     "CHA": 10,
        # },
        # "druid": {
        #     "STR": 8,
        #     "DEX": 14,
        #     "CON": 14,
        #     "INT": 12,
        #     "WIS": 15,
        #     "CHA": 8,
        # },
        "fighter": {
            "STR": 15,
            "DEX": 13,
            "CON": 14,
            "INT": 10,
            "WIS": 10,
            "CHA": 10,
        },
        # "monk": {
        #     "STR": 8,
        #     "DEX": 15,
        #     "CON": 14,
        #     "INT": 10,
        #     "WIS": 15,
        #     "CHA": 8,
        # },
        # "paladin": {
        #     "STR": 15,
        #     "DEX": 8,
        #     "CON": 15,
        #     "INT": 8,
        #     "WIS": 8,
        #     "CHA": 15,
        # },
        # "ranger": {
        #     "STR": 8,
        #     "DEX": 15,
        #     "CON": 14,
        #     "INT": 10,
        #     "WIS": 15,
        #     "CHA": 8,
        # },
        # "rogue": {
        #     "STR": 8,
        #     "DEX": 15,
        #     "CON": 14,
        #     "INT": 11,
        #     "WIS": 12,
        #     "CHA": 12,
        # },
        # "sorcerer": {
        #     "STR": 8,
        #     "DEX": 14,
        #     "CON": 14,
        #     "INT": 10,
        #     "WIS": 10,
        #     "CHA": 15,
        # },
        # "warlock": {
        #     "STR": 8,
        #     "DEX": 14,
        #     "CON": 14,
        #     "INT": 10,
        #     "WIS": 10,
        #     "CHA": 15,
        # },
        # "wizard": {
        #     "STR": 8,
        #     "DEX": 14,
        #     "CON": 14,
        #     "INT": 15,
        #     "WIS": 12,
        #     "CHA": 8,
        # },
    }
    return scores_dict[character_class]


default_health = {
    "current": 12,
    "max": 12,
    "temporary": 0,
    "conditions": [],
    "death_saves": {"successes": 0, "failures": 0},
}

default_appearance = {
    "description": "Average",
    "height": "5'9",
    "weight": "180 lbs",
    "eyes": "Brown",
    "skin": "Tan",
    "hair": "Black",
    "features": "Scar on left cheek",
}

# def ability_score_or_improvement_choices(
#         ability_restrictions: Annotated[List[str], "Limitations like maxed out ability scores"],
#         feat_restrictions: Annotated[List[str], "Limitations lik ealready having a feat"
# ) -> Dict[str, Any]:


def ability_score_improvement_options(
    current_ability_scores: Annotated[
        Dict[str, int], "Current ability scores, for determining maxes"
    ],
    amount_of_improvement: Annotated[int, "Amount of improvement"] = 1,
) -> List[str]:
    options = []
    for ability, score in current_ability_scores.items():
        if amount_of_improvement + score <= 20:
            options.append(ability)
    return options


def feat_options(
    current_feats: Annotated[
        List[str], "Current feats, for determining if a feat can be taken"
    ],
) -> List[str]:
    options = []
    for feat in feat_names():
        if feat not in current_feats:
            options.append(feat)
    return options


def ability_score_improvement_or_feat_options(
    current_ability_scores: Annotated[
        Dict[str, int], "Current ability scores, for determining maxes"
    ],
    current_feats: Annotated[
        List[str], "Current feats, for determining if a feat can be taken"
    ],
    amount_of_improvement: Annotated[int, "Amount of improvement"] = 1,
) -> Dict[str, Any]:
    return {
        "Ability Score Improvement": {
            "choices": 2,
            "options": ability_score_improvement_options(
                current_ability_scores, amount_of_improvement
            ),
        },
        "Feat": {"choices": 1, "options": feat_options(current_feats)},
    }


class_list = [
    "Barbarian",
    "Fighter",
]

skills = [
    "Acrobatics",
    "Animal Handling",
    "Arcana",
    "Athletics",
    "Deception",
    "History",
    "Insight",
    "Intimidation",
    "Investigation",
    "Medicine",
    "Nature",
    "Perception",
    "Performance",
    "Persuasion",
    "Religion",
    "Sleight of Hand",
    "Stealth",
    "Survival",
]


def skill_choices(
    current_skills: Annotated[List[str], "Current skill proficiencies"],
    subset: Annotated[
        List[str], "A subset of choices to present (ex. cleric skills)"
    ] = skills,
) -> List[str]:
    options = []
    for skill in subset:
        if skill not in current_skills:
            options.append(skill)
    return options


def class_level_choices(character_sheet) -> Dict[str, Any]:
    current_class_levels = character_sheet.class_levels
    next_class_levels = {}

    for class_name in class_list:
        next_class_levels[class_name] = 1

    # iterate through current_class_levels, and get the max level for each class
    for class_level in current_class_levels:
        class_name = class_level["name"]
        level_number = class_level["level"]
        if class_name in next_class_levels:
            if level_number >= next_class_levels[class_name]:
                next_class_levels[class_name] = level_number + 1

    class_level_choices = {
        "Barbarian": {
            1: {
                "proficiencies": {
                    "skills": {
                        "name": "Barbarian Skills",
                        "choices": 2,
                        "options": [
                            "Animal Handling",
                            "Athletics",
                            "Intimidation",
                            "Nature",
                            "Perception",
                            "Survival",
                        ],
                    }
                }
            }
        },
        "Fighter": {
            1: {
                "proficiencies": {
                    "skills": {
                        "name": "Fighter Skills",
                        "choices": 2,
                        "options": [
                            "Acrobatics",
                            "Animal Handling",
                            "Athletics",
                            "History",
                            "Insight",
                            "Intimidation",
                            "Perception",
                            "Survival",
                        ],
                    },
                },
                "features": {
                    "Fighting Style": {
                        "name": "Fighting Style",
                        "choices": 1,
                        "options": [
                            "Archery",
                            "Blind Fighting",
                            "Defense",
                            "Dueling",
                            "Great Weapon Fighting",
                            "Interception",
                            "Protection",
                            "Superior Technique",
                            "Thrown Weapon Fighting",
                            "Two-Weapon Fighting",
                            "Unarmed Fighting",
                        ],
                    }
                },
            },
            3: {
                "subclass": {
                    "name": "Martial Archetype",
                    "choices": 1,
                    "options": [
                        "Arcane Archer",
                        "Battle Master",
                        "Cavalier",
                        "Champion",
                        "Eldritch Knight",
                        "Psi Warrior",
                        "Rune Knight",
                        "Samurai",
                    ],
                }
            },
            4: {
                "ability_score_improvement_or_feat": ability_score_improvement_or_feat_options(
                    character_sheet.ability_scores, character_sheet.feats
                )
            },
            6: {
                "ability_score_improvement_or_feat": ability_score_improvement_or_feat_options(
                    character_sheet.ability_scores, character_sheet.feats
                )
            },
            8: {
                "ability_score_improvement_or_feat": ability_score_improvement_or_feat_options(
                    character_sheet.ability_scores, character_sheet.feats
                )
            },
        },
    }

    # replace the values in next_class_levels with the class_level_choices for each class and level
    for class_name, next_level in next_class_levels.items():
        next_class_levels[class_name] = class_level_choices[class_name][next_level]

    return next_class_levels


base_class_level_properties = {
    "fighter": [
        {
            "hit_die": "1d10",
            "hit_points_at_first_level": "10 + CON modifier",
            "proficiencies": {
                "weapons_and_armor": [
                    "All armor",
                    "Shields",
                    "Simple weapons",
                    "Martial weapons",
                ],
                "tools": [],
                "saving_throws": ["STR", "CON"],
                "skills": [],
                "languages": [],
            },
            "features": ["Second Wind"],
        },
        {
            "addit_hit_die": "1d10",
            "addit_hit_points": "6 + CON modifier",
            "features": ["Action Surge"],
        },
        {
            "addit_hit_die": "1d10",
            "addit_hit_points": "6 + CON modifier",
            "features": ["Martial Archetype"],
        },
    ]
}

logger.debug("***** Importing models/character_sheet.py")


class CharacterSheet(Base):

    __tablename__ = "character_sheets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    pronouns: Mapped[str] = mapped_column(String(255), default="they/them")
    alignment: Mapped[str] = mapped_column(String(255), default="Neutral")
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    race_id: Mapped[int] = mapped_column(ForeignKey("races.id"))
    race_choices: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, default={}, nullable=True
    )
    class_levels: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB, default=default_classes, nullable=True
    )
    background_id: Mapped[int] = mapped_column(ForeignKey("backgrounds.id"))
    background_choices: Mapped[Dict[str, Any]] = mapped_column(JSONB, default={})
    appearance: Mapped[str] = mapped_column(JSONB, default=default_appearance)
    base_ability_scores: Mapped[Dict[str, int]] = mapped_column(
        JSONB, default=default_ability_scores("fighter")
    )
    health: Mapped[Dict[str, Any]] = mapped_column(JSONB, default=default_health)
    inventory: Mapped[List[str]] = mapped_column(JSONB, default=[])
    roleplaying_traits: Mapped[str] = mapped_column(JSONB, default={})
    backstory: Mapped[str] = mapped_column(JSONB, default={})
    level_up_system: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, default=default_level_up_system
    )
    temporary_changes: Mapped[str] = mapped_column(JSONB, default={})
    # Relationships
    campaigns: Mapped[List["Campaign"]] = relationship(
        secondary=campaign_pcs_table, back_populates="pcs"
    )

    def compile_proficiency_type(
        self,
        proficiency_type: Annotated[
            str, "one of skills, languages, tools, weapons_and_armor, saving_throws"
        ],
    ) -> List[str]:
        proficiencies = set()

        # merge in racial skill proficiencies
        for proficiency in self.race.get("proficiencies", {}).get(proficiency_type, []):
            proficiencies.add(proficiency)
        for class_level in self.class_levels:
            for proficiency in (
                class_level.get("selections", {})
                .get("proficiencies", {})
                .get(proficiency_type, [])
            ):
                proficiencies.add(proficiency)
            for proficiency in class_level.get("proficiencies", {}).get(
                proficiency_type, []
            ):
                proficiencies.add(proficiency)
        for background_proficiency in (
            self.background.get("selections", {})
            .get("proficiencies", {})
            .get(proficiency_type, [])
        ):
            proficiencies.add(background_proficiency)

        return list(proficiencies)

    def proficiencies(self) -> Dict[str, List[str]]:
        return {
            "skills": self.compile_proficiency_type("skills"),
            "languages": self.compile_proficiency_type("languages"),
            "tools": self.compile_proficiency_type("tools"),
            "weapons_and_armor": self.compile_proficiency_type("weapons_and_armor"),
            "saving_throws": self.compile_proficiency_type("saving_throws"),
        }

    def ability_scores(self) -> Dict[str, int]:
        ability_scores = self.base_ability_scores

        for ability, increase in self.race.ability_bonuses:
            ability_scores[ability] += increase
        for ability, increase in self.race.get("selections", {}).get(
            "ability_score_increases", {}
        ):
            ability_scores[ability] += increase
        for class_level in self.class_levels:
            for ability, increase in class_level.get("ability_score_increases", {}):
                ability_scores[ability] += increase
            for ability, increase in class_level.get("selections", {}).get(
                "ability_score_increases", {}
            ):
                ability_scores[ability] += increase
            for ability, increase in (
                class_level.get("selections", {})
                .get("ability_score_increase_or_feat", {})
                .get("ability_score_increases", {})
            ):
                ability_scores[ability] += increase

        return ability_scores
