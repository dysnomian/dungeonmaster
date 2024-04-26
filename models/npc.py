from typing import TYPE_CHECKING, Set

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped, relationship

from utils.logging import logger
from models.base import Base
from models.campaign_npcs_table import campaign_npcs_table

logger.debug("***** Importing models/npc.py")

if TYPE_CHECKING:
    from models.location import Location
    from models.stat_block import StatBlock
    from models.campaign import Campaign
else:
    Location = "Location"
    StatBlock = "StatBlock"
    Campaign = "Campaign"


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
    gender: Mapped[str] = mapped_column(String(255), default="non-binary")
    pronouns: Mapped[str] = mapped_column(String(255), default="they/them")
    race: Mapped[str] = mapped_column(String(255), default="human")
    alignment_code: Mapped[str] = mapped_column(String(255), default="N")
    description: Mapped[str] = mapped_column(JSONB, default={})
    personality_traits: Mapped[str] = mapped_column(JSONB, default={})
    plot_hooks: Mapped[str] = mapped_column(JSONB, default={})
    notes: Mapped[str] = mapped_column(JSONB, default={})
    backstory: Mapped[str] = mapped_column(JSONB, default={})
    current_condition: Mapped[str] = mapped_column(JSONB, default={})
    current_location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=True
    )
    # Relationships
    current_location: Mapped[Location] = relationship(
        Location, back_populates="inhabitants"
    )
    stat_block: Mapped[StatBlock] = relationship(StatBlock)

    @property
    def alignment(self) -> str:
        return {
            "L": "Lawful",
            "N": "Neutral",
            "C": "Chaotic",
            "G": "Good",
            "E": "Evil",
            "CG": "Chaotic Good",
            "CN": "Chaotic Neutral",
            "CE": "Chaotic Evil",
            "LG": "Lawful Good",
            "LN": "Lawful Neutral",
            "LE": "Lawful Evil",
            "NG": "Neutral Good",
            "NE": "Neutral Evil",
        }.get(self.alignment_code, "Neutral")

    def __repr__(self):
        return f"<Npc full_name='{self.full_name}' stat_block='{self.stat_block}' gender='{self.gender}' race='{self.race}'>"
