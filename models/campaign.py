# CREATE TABLE
#   public.campaigns (
#     id serial NOT NULL,
#     locations jsonb NOT NULL,
#     story jsonb NOT NULL,
#     game_id integer NULL
#   );

# ALTER TABLE
#   public.campaigns
# ADD
#   CONSTRAINT campaigns_pkey PRIMARY KEY (id)

import json

from typing import Any, TYPE_CHECKING, Set, List

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import JSONB

from utils.logging import logger
from models.base import Base

from models.campaign_pcs_table import campaign_pcs_table
from models.campaign_npcs_table import campaign_npcs_table

if TYPE_CHECKING:
    from models.character_sheet import CharacterSheet
    from models.game import Game
    from models.npc import Npc
else:
    CharacterSheet = "CharacterSheet"
    Game = "Game"
    Npc = "Npc"

story_default = json.dumps(
    {
        "premise": "",
        "elevator_pitch": "",
        "primary_goal": "",
        "steps": [],
        "obstacles": [],
    }
)


logger.debug("***** Importing models/campaign.py")


class Campaign(Base):

    def __init__(self, **kw: Any):
        super().__init__(**kw)

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    story: Mapped[dict[str, Any]] = mapped_column(JSONB, default=story_default)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=True)
    # Relationships
    npcs: Mapped[Set["Npc"]] = relationship(
        secondary=campaign_npcs_table,
    )
    pcs: Mapped[List["CharacterSheet"]] = relationship(
        secondary=campaign_pcs_table,
    )
    game: Mapped[Game] = relationship(back_populates="campaign")
