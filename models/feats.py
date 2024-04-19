from typing import List, Any, Dict

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped

from models.base import Base


class Feat(Base):
    __tablename__ = "feats"

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(ForeignKey("sources.id"))
    source_page: Mapped[int] = mapped_column(Integer, nullable=True)
    prerequisites: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    ability: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    additional_spells: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    entries: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    tool_proficiencies: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    skill_proficiencies: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    language_proficiencies: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
