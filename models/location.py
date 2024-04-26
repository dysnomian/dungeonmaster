from typing import TYPE_CHECKING, List

from sqlalchemy import String, Integer, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql.schema import ForeignKey

from models.base import Base

if TYPE_CHECKING:
    from models.npc import Npc
else:
    Npc = "Npc"


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String, default="", nullable=True)
    location_type: Mapped[str] = mapped_column(String(255))
    notes: Mapped[str] = mapped_column(JSONB, default={})
    inhabitants: Mapped[List[Npc]] = relationship(
        "Npc", back_populates="current_location"
    )
    edges: Mapped[List["Edge"]] = relationship(
        "Edge", foreign_keys="[Edge.from_location_id,Edge.to_location_id]"
    )


class Edge(Base):
    __tablename__ = "edges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String, default="")
    from_location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"))
    to_location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"))
    hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    transparent: Mapped[bool] = mapped_column(Boolean, default=False)
    to_location: Mapped[Location] = relationship(
        "Location", foreign_keys=[to_location_id], back_populates="edges"
    )
    from_location: Mapped[Location] = relationship(
        "Location", foreign_keys=[from_location_id], back_populates="edges"
    )
