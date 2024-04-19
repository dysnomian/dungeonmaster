from sqlalchemy import Table, Column, Integer, Boolean, String, MetaData, Identity, text
from sqlalchemy.orm import Session


from db import engine
from models.base import Base

from utils.source_importer import import_sources
from utils.spell_importer import import_all_spells
from utils.background_importer import import_all_backgrounds
from utils.race_importer import import_all_races

Base.metadata.create_all(engine)

import_sources()
import_all_spells()
import_all_races()
import_all_backgrounds()

from models.campaign import Campaign
from models.game_session import GameSession
from models.game import Game
from models.background import Background
from models.spell import Spell
from models.player import Player
from models.character_sheet import CharacterSheet


Base.metadata.create_all(engine)

# Import data


# # Create test data

with Session(engine) as sesh:
    player = Player(
        name="Liss",
        ask_first=["Graphic Gore", "Romance", "Sexual Content"],
        veils=["Racism", "Homophobia", "Torture", "Animal Cruelty", "Cannibalism"],
        lines=[
            "Suicide",
            "Sexual Assault",
            "Child Abuse",
            "Transphobia",
            "Police Brutality",
        ],
        likes=["Lore", "Cute Animals"],
        loves=["Comedy"],
    )
    sesh.add(player)
    sesh.commit()

    game = Game(
        name="Test Game",
        player_id=1,
        rules_set="D&D 5e",
        game_length__sessions=1,
        session_length__responses=30,
        tone="Comedic, Light-hearted",
        difficulty="Easy",
        setting="Fairy Tale",
        npc_death_allowed=True,
        pc_death_allowed=True,
        rule_modifications={
            "use_feat_prereqs": False,
            "optional_class_features": True,
            "advancement_system": "xp",
            "ability_score_generation": {"type": "Point Buy"},
        },
    )

    campaign = Campaign(
        story={
            "summary": "Our hero must rescue the princess from the dragon",
            "primary_goal": "Rescue the princess from the dragon in the castle.",
            "steps": [
                "Leave the small village",
                "Learn about the location of the princess",
                "Rescue the fairy disguised as an old woman from the goblins",
                "Get the magic sword",
                "Defeat the ogre blocking the road",
                "Travel to the castle",
                "Defeat the dragon",
            ],
            "obstacles": [],
        },
        game_id=1,
    )
    sesh.add(game)
    sesh.commit()

    # character_sheet = CharacterSheet(
    #     game_id="1",
    #     name="Tes'Tcharak'Tor",
    #     alignment="Neutral Good",
    #     player_id=1,
    #     race={
    #         "name": "Variant Human",
    #         "languages": ["Common", "Goblin"],
    #         "ability_score_increases": {"STR": 1, "DEX": 1},
    #         "proficiencies": {
    #             "skills": ["Perception"],
    #         },
    #         "feats": ["Alert"],
    #     },
    #     class_levels=[
    #         {
    #             "name": "Fighter",
    #             "level": 1,
    #             "selections": {
    #                 "fighting_style": "Dueling",
    #                 "proficiencies": {"skills": ["Athletics", "Insight"]},
    #             },
    #         }
    #     ],
    #     base_ability_scores={
    #         "STR": 15,
    #         "DEX": 13,
    #         "CON": 14,
    #         "INT": 10,
    #         "WIS": 10,
    #         "CHA": 10,
    #     },
    #     background={
    #         "name": "Soldier",
    #         "selections": {
    #             "proficiencies": {"skills": ["Investigation"], "tools": ["Dice Set"]}
    #         },
    #     },
    #     appearance={
    #         "description": "Average",
    #         "height": "5'9",
    #         "weight": "180 lbs",
    #         "eyes": "Brown",
    #         "skin": "Tan",
    #         "hair": "Black",
    #         "features": "Scar on left cheek",
    #     },
    # )

    # sesh.add(character_sheet)

    # sesh.commit()
