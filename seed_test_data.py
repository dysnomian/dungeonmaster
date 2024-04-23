from sqlalchemy.orm import Session


from db import engine
from models.base import Base

from utils.source_importer import import_sources
from utils.spell_importer import import_all_spells
from utils.background_importer import import_all_backgrounds
from utils.race_importer import import_all_races
from utils.stat_block_importer import import_all_stat_blocks

Base.metadata.create_all(engine)

import_sources()
import_all_spells()
import_all_races()
import_all_backgrounds()
import_all_stat_blocks()

from models.player import Player
from models.game import Game
from models.game_session import GameSession
from models.campaign import Campaign
from models.character_sheet import CharacterSheet
from models.npc import Npc
from models.race import Race
from models.background import Background
from models.location import Location
from models.stat_block import StatBlock

from utils.npc_generator import generate_npc

Base.metadata.create_all(engine)

# Create test data

with Session(engine) as sesh:
    player = sesh.query(Player).filter_by(name="Liss").first()
    if not player:
        print("***************** Creating test player")
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
        print("***************** Creating test game")
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
    if not campaign:
        print("***************** Creating test campaign")
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

    human = sesh.query(Race).filter_by(name="Human").first()  # id: 72
    soldier = sesh.query(Background).filter_by(name="Soldier").first()  # id: 108

    character_sheet = (
        sesh.query(CharacterSheet).filter_by(name="Tes'Tcharak'Tor").first()
    )
    if not character_sheet:
        print("***************** Creating test character sheet")
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
        )

        sesh.add(character_sheet)
        sesh.commit()

    castle = sesh.query(Location).filter_by(name="Castle").first()
    if not castle:
        print("***************** Creating test location")
        castle = Location(
            name="Castle",
            location_type="Large building",
            description="A large stone castle wall with a moat and drawbridge.",
        )
        sesh.add(castle)
        sesh.commit()

    keep = sesh.query(Location).filter_by(name="Keep").first()
    if not keep:
        keep = Location(
            name="Castle Keep",
            location_type="Building",
            description="A large central keep.",
            inside_of=castle,
        )
        sesh.add(keep)
        sesh.commit()

    village = sesh.query(Location).filter_by(name="Humbleton Village").first()
    if not village:
        village = Location(
            name="Humbleton Village",
            location_type="Village",
            description="A small village with a few houses and a tavern.",
        )
        sesh.add(village)
        sesh.commit()

    noble = sesh.query(StatBlock).filter_by(name="Noble").first()  # id: 280

    princess = sesh.query(Npc).filter_by(first_name="Violet").first()

    if not princess:
        print("***************** Creating test NPC")
        princess = Npc(
            first_name="Violet",
            full_name="Princess Violet",
            description="A beautiful princess with long golden hair and a kind smile.",
            stat_block_id=noble.id,
            pronouns="she/her",
            race="Human",
            alignment="LG",
            campaigns=[campaign],
            current_location_id=keep.id,
        )

        sesh.add(princess)
        sesh.commit()

    black_dragon = sesh.query(StatBlock).filter_by(name="Adult Black Dragon").first()
    dragon = sesh.query(Npc).filter_by(first_name="Kalvaxis").first()

    if not dragon:
        print("***************** Creating test NPC")
        dragon = Npc(
            first_name="Kalvaxis",
            description="An evil black dragon.",
            stat_block_id=black_dragon.id,
            pronouns="he/him",
            race="Dragon",
            alignment="CE",
            campaigns=[campaign],
            current_location_id=castle.id,
        )

        sesh.add(dragon)
        sesh.commit()

    generate_npc()

    game_session = sesh.query(GameSession).filter_by(game_id=game.id).first()
    if not game_session:
        print("***************** Creating game session")
        game_session = GameSession(
            game_id=game.id,
            current_location_id=village.id,
            current_time="Morning",
        )
        sesh.add(game_session)
        sesh.commit()

    npcs = sesh.query(Npc).filter(Npc.campaigns.any(id=campaign.id)).all()
