# DB Table: backgrounds
# CREATE TABLE
#   public.backgrounds (
#     id serial NOT NULL,
#     name character varying NOT NULL,
#     source_id integer NULL,
#     source_page integer NULL,
#     skill_proficiencies jsonb NULL,
#     tool_proficiencies jsonb NULL,
#     language_proficiencies jsonb NULL,
#     starting_equipment jsonb NULL,
#     entries jsonb NULL,
#     additional_spells jsonb NULL
#   );

# ALTER TABLE
#   public.backgrounds
# ADD
#   CONSTRAINT backgrounds_pkey PRIMARY KEY (id)

from typing import List

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped

from utils.logging import logger
from models.base import Base


logger.debug("Importing models/background.py")


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
