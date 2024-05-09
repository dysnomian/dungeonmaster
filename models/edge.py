from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.sql.schema import ForeignKey

from models.base import Base

if TYPE_CHECKING:
    from models.location import Location
else:
    Location = "Location"

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
        "Location", foreign_keys='[Location.id]', back_populates="edges", primaryjoremote_side='Location.id'
    )
    from_location: Mapped[Location] = relationship(
        "Location", foreign_keys='[Location.id]', back_populates="edges"
    )
