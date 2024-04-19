from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column, Mapped

from models.base import Base

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


class NPC(Base):
    __tablename__ = "npcs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    stat_block: Mapped[str] = mapped_column(JSONB, default=default_stat_block)
    pronouns: Mapped[str] = mapped_column(String(255), default="they/them")
    race: Mapped[str] = mapped_column(String(255), default="Human")
    alignment: Mapped[str] = mapped_column(String(255), default="Neutral")
    description: Mapped[str] = mapped_column(JSONB, default={})
    personality_traits: Mapped[str] = mapped_column(JSONB, default={})
    plot_hooks: Mapped[str] = mapped_column(JSONB, default={})
    notes: Mapped[str] = mapped_column(JSONB, default={})
