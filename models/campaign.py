import json

from typing import Any, List, TYPE_CHECKING

from sqlalchemy import ForeignKey, Column, Table, Integer
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB

from utils.logging import logger
from models.base import Base

if TYPE_CHECKING:
    from models.character_sheet import CharacterSheet
    from models.game import Game
    from models.npc import Npc

story_default = json.dumps(
    {
        "premise": "",
        "elevator_pitch": "",
        "primary_goal": "",
        "steps": [],
        "obstacles": [],
    }
)

campaign_pcs_table = Table(
    "campaign_pcs",
    Base.metadata,
    Column("campaign_id", ForeignKey("campaigns.id"), primary_key=True),
    Column("character_sheet_id", ForeignKey("character_sheets.id"), primary_key=True),
)

campaign_npcs_table = Table(
    "campaign_npcs",
    Base.metadata,
    Column("campaign_id", ForeignKey("campaigns.id"), primary_key=True),
    Column("npc_id", ForeignKey("npcs.id"), primary_key=True),
)


logger.debug("***** Importing models/campaign.py")


class Campaign(Base):
    def __init__(self, **kw: Any):
        super().__init__(**kw)

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    locations: Mapped[List[Any]] = mapped_column(JSONB, default=[])
    npcs: Mapped[List["Npc"]] = relationship(
        secondary=campaign_npcs_table, back_populates="campaigns"
    )
    story: Mapped[dict[str, Any]] = mapped_column(JSONB, default=story_default)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=True)
    game: Mapped["Game"] = relationship("Game", back_populates="campaign")
    player_characters: Mapped[List["CharacterSheet"]] = relationship(
        secondary=campaign_pcs_table, back_populates="campaigns"
    )
