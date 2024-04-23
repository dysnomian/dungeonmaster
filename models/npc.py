from typing import List, TYPE_CHECKING, Union, Dict, Any

import random

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column, Mapped

from utils.logging import logger
from models.base import Base
from models.campaign import campaign_npcs_table

if TYPE_CHECKING:
    from models.campaign import Campaign
    from models.location import Location
    from models.stat_block import StatBlock

default_stat_block = {
    "name": "Commoner",
    "size": "M",
    "type": {"type": "Humanoid", "tags": ["any race"]},
    "alignment": ["any"],
    "ac": [10],
    "hp": {"average": 4, "formula": "1d8"},
    "speed": {"walk": 30},
    "str": 10,
    "dex": 10,
    "con": 10,
    "int": 10,
    "wis": 10,
    "cha": 10,
    "passive_perception": 10,
    "languages": ["any"],
    "cr": 0,
    "actions": [
        {
            "name": "Club",
            "entries": "Melee Weapon Attack: +2 to hit, reach 5 ft., one target. Hit: 2 (1d4) bludgeoning damage.",
        }
    ],
}


logger.debug("***** Importing models/npc.py")


class Npc(Base):
    __tablename__ = "npcs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    surname: Mapped[str] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=True)
    stat_block_id: Mapped[int] = mapped_column(
        ForeignKey("stat_blocks.id"), nullable=True
    )
    stat_block: Mapped["StatBlock"] = relationship("StatBlock")
    gender: Mapped[str] = mapped_column(String(255), default="non-binary")
    pronouns: Mapped[str] = mapped_column(String(255), default="they/them")
    race: Mapped[str] = mapped_column(String(255), default="human")
    alignment: Mapped[str] = mapped_column(String(255), default="Neutral")
    description: Mapped[str] = mapped_column(JSONB, default={})
    personality_traits: Mapped[str] = mapped_column(JSONB, default={})
    plot_hooks: Mapped[str] = mapped_column(JSONB, default={})
    notes: Mapped[str] = mapped_column(JSONB, default={})
    backstory: Mapped[str] = mapped_column(JSONB, default={})
    current_condition: Mapped[str] = mapped_column(JSONB, default={})
    current_location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=True
    )
    current_location: Mapped["Location"] = relationship(
        "Location", back_populates="inhabitants"
    )

    campaigns: Mapped[List["Campaign"]] = relationship(
        secondary=campaign_npcs_table, back_populates="npcs"
    )

    def __repr__(self):
        return f"<Npc {self.first_name} {self.surname} {self.gender} {self.race} {self.alignment}>"
