from typing import List, Dict, Any, Union

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped
from models.base import Base

senses_default = {
    "darkvision": 0,
    "blindsight": 0,
    "tremorsense": 0,
    "truesight": 0,
}

proficiencies_default = {
    "weapons_and_armor": [],
    "tools": [],
    "saving_throws": [],
    "skills": [],
    "languages": [],
}

speed_default = {"walk": 30, "fly": 0, "swim": 0, "climb": 0}


class Race(Base):
    __tablename__ = "races"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    basic_rules: Mapped[bool] = mapped_column(nullable=True, default=False)
    legacy: Mapped[bool] = mapped_column(nullable=True, default=False)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), nullable=True)
    source_page: Mapped[int] = mapped_column(Integer, nullable=True)
    size: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=["Medium"])
    speed: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=True, default=speed_default
    )
    ability_bonuses: Mapped[Dict[str, int]] = mapped_column(
        JSONB, nullable=True, default={}
    )
    entries: Mapped[List[Any]] = mapped_column(JSONB, nullable=True, default=[])
    resistances: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    additional_spells: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True, default=[]
    )
    age: Mapped[Union[str, Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True, default=""
    )
    senses: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=True, default=senses_default
    )
    creature_types: Mapped[List[str]] = mapped_column(
        JSONB, nullable=True, default=["humanoid"]
    )
    trait_tags: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    condition_immunities: Mapped[List[str]] = mapped_column(
        JSONB, nullable=True, default=[]
    )
    resistances: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    immunities: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    vulnerabilities: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    proficiencies: Mapped[Dict[str, List[str]]] = mapped_column(
        JSONB, nullable=True, default=proficiencies_default
    )


class RaceVariants(Base):
    __tablename__ = "race_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    basic_rules: Mapped[bool] = mapped_column(nullable=True, default=False)
    legacy: Mapped[bool] = mapped_column(nullable=True, default=False)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), nullable=True)
    source_page: Mapped[int] = mapped_column(Integer, nullable=True)
    size: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=["Medium"])
    speed: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=True, default=speed_default
    )
    ability_bonuses: Mapped[Dict[str, int]] = mapped_column(
        JSONB, nullable=True, default={}
    )
    entries: Mapped[List[Any]] = mapped_column(JSONB, nullable=True, default=[])
    resistances: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    additional_spells: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True, default=[]
    )
    age: Mapped[Union[str, Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True, default=""
    )
    senses: Mapped[Dict[str, Any]] = mapped_column(
        JSONB, nullable=True, default=senses_default
    )
    creature_types: Mapped[List[str]] = mapped_column(
        JSONB, nullable=True, default=["humanoid"]
    )
    trait_tags: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    condition_immunities: Mapped[List[str]] = mapped_column(
        JSONB, nullable=True, default=[]
    )
    resistances: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    immunities: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    vulnerabilities: Mapped[List[str]] = mapped_column(JSONB, nullable=True, default=[])
    proficiencies: Mapped[Dict[str, List[str]]] = mapped_column(
        JSONB, nullable=True, default=proficiencies_default
    )
    parent_race_id: Mapped[int] = mapped_column(ForeignKey("races.id"), nullable=False)
    parent_race_source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    alias: Mapped[Any] = mapped_column(JSONB, nullable=True)
    overwrite: Mapped[Any] = mapped_column(JSONB, nullable=True)
