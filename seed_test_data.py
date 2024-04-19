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
from models.race import Race
from models.player import Player
from models.character_sheet import CharacterSheet
from models.npc import Npc


Base.metadata.create_all(engine)

# Import data


# # Create test data

with Session(engine) as sesh:
    player = sesh.query(Player).filter_by(name="Liss").first()
    if not player:
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

    game = sesh.query(Game).filter_by(name="Test Game").first()
    if not game:
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
        sesh.add(game)
        sesh.commit()

    campaign = sesh.query(Campaign).filter_by(game_id=game.id).first()
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
        game_id=game.id,
    )
    sesh.add(campaign)
    sesh.commit()

    human = sesh.query(Race).filter_by(name="Human").first()
    soldier = sesh.query(Background).filter_by(name="Soldier").first()

    character_sheet = (
        sesh.query(CharacterSheet).filter_by(name="Tes'Tcharak'Tor").first()
    )
    if not character_sheet:
        character_sheet = CharacterSheet(
            name="Tes'Tcharak'Tor",
            alignment="NG",
            player_id=player.id,
            race_id=human.id,
            class_levels=[
                {
                    "name": "Fighter",
                    "level": 1,
                    "selections": {
                        "fighting_style": "Dueling",
                        "proficiencies": {"skills": ["Athletics", "Insight"]},
                    },
                }
            ],
            base_ability_scores={
                "STR": 15,
                "DEX": 13,
                "CON": 14,
                "INT": 10,
                "WIS": 10,
                "CHA": 10,
            },
            background_id=soldier.id,
            appearance={
                "description": "Average",
                "height": "5'9",
                "weight": "180 lbs",
                "eyes": "Brown",
                "skin": "Tan",
                "hair": "Black",
                "features": "Scar on left cheek",
            },
            campaigns=[campaign.id],
        )

        sesh.add(character_sheet)
        sesh.commit()

    game_session = sesh.query(GameSession).filter_by(game_id=game.id).first()
    if not game_session:
        game_session = GameSession(
            game_id=game.id,
            current_campaign_id=campaign.id,
            current_character_id=character_sheet.id,
            current_location="Village",
            current_time="Morning",
        )
        sesh.add(game_session)
        sesh.commit()

    npcs = sesh.query(Npc).filter(Npc.campaigns.any(id=campaign.id)).all()
