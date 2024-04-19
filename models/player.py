from typing import List

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, mapped_column, Mapped
from models.base import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.character_sheet import CharacterSheet
    from models.game import Game


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    veils: Mapped[List[str]] = mapped_column(JSONB, default=[])
    lines: Mapped[List[str]] = mapped_column(JSONB, default=[])
    ask_first: Mapped[List[str]] = mapped_column(JSONB, default=[])
    likes: Mapped[List[str]] = mapped_column(JSONB, default=[])
    loves: Mapped[List[str]] = mapped_column(JSONB, default=[])
    games: Mapped[List["Game"]] = relationship(
        "Game", back_populates="player", cascade="all, delete-orphan"
    )
    characters: Mapped[List["CharacterSheet"]] = relationship(
        "CharacterSheet", back_populates="player", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.name}, games={self.games})>"
