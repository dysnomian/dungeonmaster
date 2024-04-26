import psycopg2 as pg

from sqlalchemy import select

from typing import List, Tuple, Any

from db import session

from models.npc import Npc
from models.character_sheet import CharacterSheet
from models.game import Game
from models.player import Player
from models.campaign_pcs_table import campaign_pcs_table
from models.campaign_npcs_table import campaign_npcs_table

conn = pg.connect(dbname="dungeonmaster_dev", user="dungeonmaster_dev")


# def games_for_player(player_id: int) -> List[Tuple[Any]]:
#     with conn.cursor() as cursor:
#         cursor.execute(
#             """
#             SELECT *
#             FROM games
#             WHERE player_id = %s
#             """,
#             (player_id,),
#         )
#         return cursor.fetchall()


def games_for_player(player_id: int):
    return (
        session.execute(select(Game).where(Game.player_id == player_id)).scalars().all()
    )


# def npcs_for_campaign(campaign_id):
#     stmt = (
#         select(Npc)
#         .join(campaign_npcs_table)
#         .where(campaign_npcs_table.c.campaign_id == campaign_id)
#     )
#     return session.execute(stmt).scalars().all()


# def pcs_for_campaign(campaign_id):
#     stmt = (
#         select(CharacterSheet)
#         .join(campaign_pcs_table)
#         .where(campaign_pcs_table.c.campaign_id == campaign_id)
#     )
#     return session.execute(stmt).scalars().all()
