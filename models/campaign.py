import json

from typing import Any, List

from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB

from models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.character_sheet import CharacterSheet
    from models.game import Game

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
    Column("campaign_id", ForeignKey("campaigns.id")),
    Column("player_character_id", ForeignKey("character_sheets.id")),
)


class Campaign(Base):
    def __init__(self, **kw: Any):
        super().__init__(**kw)

    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(primary_key=True)
    locations: Mapped[List[Any]] = mapped_column(JSONB, default=[])
    npcs: Mapped[List[Any]] = mapped_column(JSONB, default=[])
    story: Mapped[dict[str, Any]] = mapped_column(JSONB, default=story_default)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=True)
    game: Mapped["Game"] = relationship("Game", back_populates="campaign")
    player_characters: Mapped[List["CharacterSheet"]] = relationship(
        secondary=campaign_pcs_table
    )