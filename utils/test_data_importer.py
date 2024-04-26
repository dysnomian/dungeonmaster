import psycopg2

from typing import Any, List, TYPE_CHECKING

from sqlalchemy.sql import select

from db import session, engine

from models.base import Base

from utils.logging import logger

from utils.importers import IMPORT_PATH, source_dict

from models.source import Source
from models.race import Race
from models.background import Background
from models.stat_block import StatBlock

Base.metadata.create_all(engine)

conn = psycopg2.connect(
    dbname="dungeonmaster_dev",
    user="dungeonmaster_dev",
)


def test_source_presence(value: str) -> str:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM sources WHERE abbreviation = %s", (value,))
        return cursor.fetchone()


def test_race_presence(value: str) -> str:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM races WHERE name = %s", (value,))
        return cursor.fetchone()


def test_background_presence(value: str) -> str:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM backgrounds WHERE name = %s", (value,))
        return cursor.fetchone()


def test_stat_block_presence(value: str) -> str:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM stat_blocks WHERE name = %s", (value,))
        return cursor.fetchone()


def import_test_data():
    phb = test_source_presence("PHB")
    if not phb:
        phb = Source(
            id=1,
            name="Player's Handbook",
            abbreviation="PHB",
            author="Wizards RPG Team",
            group="core",
        )
        session.add(phb)
        session.commit()

    dmg = test_source_presence("DMG")
    if not dmg:
        dmg = Source(
            id=2,
            name="Dungeon Master's Guide",
            abbreviation="DMG",
            author="Wizards RPG Team",
            group="core",
        )
        session.add(dmg)
        session.commit()

    human = test_race_presence("Human")
    if not human:
        human = Race(
            id=72,
            name="Human",
            source_id=1,
            source_page=29,
            size=["M"],
            speed={"walk": 30},
            age={"max": 100, "mature": 20},
            senses={"darkvision": 0},
            proficiencies={
                "skills": [],
                "languages": [{"common": True, "anyStandard": 1}],
                "weapons_and_armor": [None],
            },
            entries=[
                {
                    "name": "Age",
                    "type": "entries",
                    "entries": [
                        "Humans reach adulthood in their late teens and live less than a century."
                    ],
                },
                {
                    "name": "Size",
                    "type": "entries",
                    "entries": [
                        "Humans vary widely in height and build, from barely 5 feet to well over 6 feet tall. Regardless of your position in that range, your size is Medium."
                    ],
                },
                {
                    "name": "Languages",
                    "type": "entries",
                    "entries": [
                        "You can speak, read, and write Common and one extra language of your choice. Humans typically learn the languages of other peoples they deal with, including obscure dialects. They are fond of sprinkling their speech with words borrowed from other tongues: Orc curses, Elvish musical expressions, Dwarvish military phrases, and so on."
                    ],
                },
            ],
        )
        session.add(human)
        session.commit()

    soldier = test_background_presence("Soldier")
    if not soldier:
        soldier = Background(id=108, name="Soldier", source_id=1, source_page=140)
        session.add(soldier)
        session.commit()

    noble = test_stat_block_presence("Noble")
    if not noble:
        noble = StatBlock(
            id=282,
            name="Noble",
            source_id=1,
            source_page=136,
            sizes=["M"],
            creature_type={"tags": ["any_race"], "type": "humanoid"},
            alignments=["A"],
            ac=[{"ac": 15, "from": ["{@item breastplate|phb}"]}],
            hp={"average": 9, "formula": "2d8"},
            speed={"walk": 30},
            ability_scores={
                "STR": 11,
                "DEX": 12,
                "CON": 11,
                "INT": 12,
                "WIS": 14,
                "CHA": 16,
            },
            saving_throw_bonuses={},
            skills={"insight": "+4", "deception": "+5", "persuasion": "+5"},
            senses={},
            languages=["any two languages"],
            cr="1/8",
            traits=[],
            actions=[
                {
                    "name": "Rapier",
                    "entries": [
                        "{@atk mw} {@hit 3} to hit, reach 5 ft., one target. {@h}5 ({@damage 1d8 + 1}) piercing damage."
                    ],
                }
            ],
            reactions=[
                {
                    "name": "Parry",
                    "entries": [
                        "The noble adds 2 to its AC against one melee attack that would hit it. To do so, the noble must see the attacker and be wielding a melee weapon."
                    ],
                }
            ],
            legendary_actions=None,
            environments=["urban"],
            condition_immunities=None,
            immunities=None,
        )
        session.add(noble)
        session.commit()

    dragon = test_stat_block_presence("Adult Black Dragon")
    if not dragon:
        dragon = StatBlock(
            id=5,
            name="Adult Black Dragon",
            source_id=2,
            source_page=88,
            sizes=["H"],
            creature_type={"tags": ["dragon"], "type": "creature"},
            alignments=["C", "E"],
            ac=[{"ac": 19, "from": ["natural armor"]}],
            hp={"average": 195, "formula": "17d12 + 85"},
            speed={"fly": 80, "swim": 40, "walk": 40},
            ability_scores={
                "STR": 23,
                "DEX": 14,
                "CON": 21,
                "INT": 14,
                "WIS": 13,
                "CHA": 17,
            },
            saving_throw_bonuses={"CHA": "+8", "CON": "+10", "DEX": "+7"},
            skills={"stealth": "+7", "perception": "+11"},
            senses={"darkvision": 120, "blindsight": 60},
            languages=["Common", "Draconic"],
            cr="14",
            traits=[
                {
                    "name": "Amphibious",
                    "entries": ["The dragon can breathe air and water."],
                },
                {
                    "name": "Legendary Resistance (3/Day)",
                    "entries": [
                        "If the dragon fails a saving throw, it can choose to succeed instead."
                    ],
                },
            ],
            actions=[
                {
                    "name": "Multiattack",
                    "entries": [
                        "The dragon can use its Frightful Presence. It then makes three attacks: one with its bite and two with its claws."
                    ],
                },
                {
                    "name": "Bite",
                    "entries": [
                        "{@atk mw} {@hit 11} to hit, reach 10 ft., one target. {@h}17 ({@damage 2d10 + 6}) piercing damage plus 4 ({@damage 1d8}) acid damage."
                    ],
                },
                {
                    "name": "Claw",
                    "entries": [
                        "{@atk mw} {@hit 11} to hit, reach 5 ft., one target. {@h}13 ({@damage 2d6 + 6}) slashing damage."
                    ],
                },
                {
                    "name": "Tail",
                    "entries": [
                        "{@atk mw} {@hit 11} to hit, reach 15 ft., one target. {@h}15 ({@damage 2d8 + 6}) bludgeoning damage."
                    ],
                },
                {
                    "name": "Frightful Presence",
                    "entries": [
                        "Each creature of the dragon's choice that is within 120 feet of the dragon and aware of it must succeed on a {@dc 16} Wisdom saving throw or become {@condition frightened} for 1 minute. A creature can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success. If a creature's saving throw is successful or the effect ends for it, the creature is immune to the dragon's Frightful Presence for the next 24 hours."
                    ],
                },
                {
                    "name": "Acid Breath {@recharge 5}",
                    "entries": [
                        "The dragon exhales acid in a 60-foot line that is 5 feet wide. Each creature in that line must make a {@dc 18} Dexterity saving throw, taking 54 ({@damage 12d8}) acid damage on a failed save, or half as much damage on a successful one."
                    ],
                },
            ],
            reactions=None,
            legendary_actions=[
                {
                    "name": "Detect",
                    "entries": [
                        "The dragon makes a Wisdom ({@skill Perception}) check."
                    ],
                },
                {"name": "Tail Attack", "entries": ["The dragon makes a tail attack."]},
                {
                    "name": "Wing Attack (Costs 2 Actions)",
                    "entries": [
                        "The dragon beats its wings. Each creature within 10 feet of the dragon must succeed on a {@dc 19} Dexterity saving throw or take 13 ({@damage 2d6 + 6}) bludgeoning damage and be knocked {@condition prone}. The dragon can then fly up to half its flying speed."
                    ],
                },
            ],
            environments=["swamp"],
            condition_immunities=None,
            immunities=["acid"],
        )
        session.add(dragon)
        session.commit()

    goblin = test_stat_block_presence("Goblin")
    if not goblin:
        goblin = StatBlock(
            id=193,
            name="Goblin",
            source_id=1,
            source_page=166,
            sizes=["S"],
            creature_type={"tags": ["goblinoid"], "type": "humanoid"},
            alignments=["N", "E"],
            ac=[
                {"ac": 15, "from": ["{@item leather armor|phb}", "{@item shield|phb}"]}
            ],
            hp={"average": 7, "formula": "2d6"},
            speed={"walk": 30},
            ability_scores={
                "STR": 8,
                "DEX": 14,
                "CON": 10,
                "INT": 10,
                "WIS": 8,
                "CHA": 8,
            },
            saving_throw_bonuses={},
            skills={"stealth": "+6"},
            senses={"darkvision": 60},
            languages=["Common", "Goblin"],
            cr="1/4",
            traits=[
                {
                    "name": "Nimble Escape",
                    "entries": [
                        "The goblin can take the Disengage or Hide action as a bonus action on each of its turns."
                    ],
                }
            ],
            actions=[
                {
                    "name": "Scimitar",
                    "entries": [
                        "{@atk mw} {@hit 4} to hit, reach 5 ft., one target. {@h}5 ({@damage 1d6 + 2}) slashing damage."
                    ],
                },
                {
                    "name": "Shortbow",
                    "entries": [
                        "{@atk rw} {@hit 4} to hit, range 80/320 ft., one target. {@h}5 ({@damage 1d6 + 2}) piercing damage."
                    ],
                },
            ],
            reactions=None,
            legendary_actions=None,
            environments=["underdark", "grassland", "forest", "hill"],
            condition_immunities=None,
            immunities=None,
        )
        session.add(goblin)
        session.commit()

    ogre = test_stat_block_presence("Ogre")
    if not ogre:
        ogre = StatBlock(
            id=287,
            name="Ogre",
            source_id=1,
            source_page=237,
            sizes=["L"],
            creature_type={"tags": ["giant"], "type": "humanoid"},
            alignments=["C", "E"],
            ac=[{"ac": 11, "from": ["{@item hide armor|phb}"]}],
            hp={"average": 59, "formula": "7d10 + 21"},
            speed={"walk": 40},
            ability_scores={
                "STR": 19,
                "DEX": 8,
                "CON": 16,
                "INT": 5,
                "WIS": 7,
                "CHA": 7,
            },
            saving_throw_bonuses={},
            skills={},
            senses={"darkvision": 60},
            languages=["Common", "Giant"],
            cr="2",
            traits=[],
            actions=[
                {
                    "name": "Greatclub",
                    "entries": [
                        "{@atk mw} {@hit 6} to hit, reach 5 ft., one target. {@h}13 ({@damage 2d8 + 4}) bludgeoning damage."
                    ],
                },
                {
                    "name": "Javelin",
                    "entries": [
                        "{@atk mw,rw} {@hit 6} to hit, reach 5 ft. or range 30/120 ft., one target. {@h}11 ({@damage 2d6 + 4}) piercing damage."
                    ],
                },
            ],
            reactions=None,
            legendary_actions=None,
            environments=[
                "grassland",
                "forest",
                "swamp",
                "hill",
                "desert",
                "coastal",
                "arctic",
                "underdark",
                "mountain",
            ],
            condition_immunities=None,
            immunities=None,
        )
        session.add(ogre)
        session.commit()
