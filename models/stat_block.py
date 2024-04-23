from typing import TYPE_CHECKING, Any, Dict, List

from models.base import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB


default_ability_scores = {
    "STR": 10,
    "DEX": 10,
    "CON": 10,
    "INT": 10,
    "WIS": 10,
    "CHA": 10,
}

default_speed = {"walk": 30}
default_hp = {"average": 4, "formula": "1d8"}


class StatBlock(Base):
    __tablename__ = "stat_blocks"

    id = Column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    source_id = Column(ForeignKey("sources.id"), nullable=True)
    source_page: Mapped[int] = mapped_column(Integer, nullable=True)
    srd: Mapped[bool] = mapped_column(default=False)
    sizes: Mapped[List[str]] = mapped_column(JSONB, default=["M"])
    creature_type: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    alignments: Mapped[List[str]] = mapped_column(JSONB, default=["any"])
    ac: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    hp: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    speed: Mapped[Dict[str, Any]] = mapped_column(JSONB, nullable=True)
    ability_scores: Mapped[Dict[str, int]] = mapped_column(
        JSONB, nullable=True, default=default_ability_scores
    )
    saving_throw_bonuses: Mapped[Dict[str, int]] = mapped_column(JSONB, nullable=True)
    skills: Mapped[Dict[str, int]] = mapped_column(JSONB, nullable=True)
    senses: Mapped[Dict[str, int]] = mapped_column(JSONB, nullable=True)
    languages: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    cr: Mapped[str] = mapped_column(String, nullable=True)
    traits: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    actions: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    reactions: Mapped[List[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    legendary_actions: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )
    environments: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    condition_immunities: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    immunities: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
