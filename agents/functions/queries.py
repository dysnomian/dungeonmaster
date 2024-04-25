from db import session

from models.game import Game
from models.player import Player
from models.game_session import GameSession
from models.campaign import Campaign
from models.character_sheet import CharacterSheet
from models.background import Background
from models.race import Race
from models.location import Location
from models.npc import Npc
from models.stat_block import StatBlock

def find_game(game_id: int) -> Game:
    return session.query(Game).filter(Game.id == game_id).first()

def find_player(player_id: int) -> Player:
    return session.query(Player).filter(Player.id == player_id).first()


def find_character_sheets(player_character_ids: list[int]) -> list[CharacterSheet]:
    count = len(player_character_ids)
    return session.query(CharacterSheet).filter(
        CharacterSheet.id.in_(player_character_ids)
    ).limit(count).all()

def find_campaign(campaign_id: int) -> Campaign:
    return session.query(Campaign).filter(Campaign.id == campaign_id).first()

def update_campaign_story(game_id, story) -> Campaign:
    game = find_game(game_id)
    campaign = game.campaign
    campaign.story = story

    session.add(campaign)
    session.commit()
    return campaign

def get_current_campaign(game_id: int) -> Campaign:
    return find_game(game_id).campaign

def get_current_session(game_id: int) -> GameSession:
    game_sessions = session.query(GameSession).filter(GameSession.game_id == game_id).order_by(GameSession.created_at.desc())
    return game_sessions.first()

def get_current_location(game_id: int) -> Location:
    return get_current_session(game_id).current_location

def get_current_time(game_id: int) -> str:
    return get_current_session(game_id).current_time

def get_npc(game_id: int, npc_id: int) -> Npc:
    campaign = session.query(Game).filter(Game.id == game_id).first().campaign

    return session.query(Npc).filter(Npc.id == npc_id).filter(Npc.campaigns.contains(campaign)).first()

def get_game_tone(game_id: int) -> str:
    return session.query(Game).filter(Game.id == game_id).first().tone

def get_primary_pc(game_id: int) -> CharacterSheet:
    campaign = get_current_campaign(game_id)
    return campaign.player_characters