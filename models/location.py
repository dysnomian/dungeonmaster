from typing import List

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.schema import ForeignKey

from models.base import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(JSONB, default={})
    adjacent_location_ids: Mapped[List[int]] = mapped_column(JSONB, default=[])
    sub_location_ids: Mapped[List[int]] = mapped_column(JSONB, default=[])
    within_location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    inhabitants: Mapped[List[int]] = mapped_column(JSONB, default=[])
    notes: Mapped[str] = mapped_column(JSONB, default={})
