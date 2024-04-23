from typing import List

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped

from utils.logging import logger
from models.base import Base


logger.debug("***** Importing models/background.py")


class Background(Base):
    __tablename__ = "backgrounds"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), nullable=True)
    source_page: Mapped[int] = mapped_column(Integer, nullable=True)
    skill_proficiencies: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    tool_proficiencies: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    language_proficiencies: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    starting_equipment: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    entries: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
    additional_spells: Mapped[List[str]] = mapped_column(JSONB, nullable=True)
