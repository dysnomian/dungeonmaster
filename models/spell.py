from typing import List, Any, Dict

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped

from utils.logging import logger
from models.base import Base


logger.debug("***** Importing models/spell.py")


class Spell(Base):
    __tablename__ = "spells"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), nullable=True)
    source_page: Mapped[int] = mapped_column(Integer, nullable=True)
    range: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, default={"type": "point", "distance": {"type": "feet", "amount": 60}}
    )
    time: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    range: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    components: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    duration: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    meta: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    entries: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    scaling_level_dice: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    damage_inflict: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    saving_throw: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    misc_tags: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    area_tags: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
