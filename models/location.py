from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.schema import ForeignKey

from models.base import Base

if TYPE_CHECKING:
    from models.npc import Npc


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    location_type: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(JSONB, default={})
    # adjacent_location_ids: Mapped[List[int]] = mapped_column(JSONB, default=[])
    # contains: Mapped[List["Location"]] = relationship(
    #     "Location", backref="inside_of_location"
    # )
    # inside_of: Mapped["Location"] = relationship(
    #     "Location", backref="contains", remote_side=[id]
    # )
    # inside_of_location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    inside_of_location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id"), nullable=True
    )
    inside_of: Mapped["Location"] = relationship(
        "Location", remote_side=[inside_of_location_id]
    )
    contains: Mapped[List["Location"]] = relationship(
        "Location", foreign_keys=[inside_of_location_id], overlaps="inside_of"
    )
    inhabitants: Mapped[List["Npc"]] = relationship(
        "Npc", back_populates="current_location"
    )

    notes: Mapped[str] = mapped_column(JSONB, default={})
