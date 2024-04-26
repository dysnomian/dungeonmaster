from typing import List

from sqlalchemy import String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import mapped_column, Mapped, relationship

from utils.logging import logger
from models.base import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.character_sheet import CharacterSheet
    from models.game import Game
else:
    CharacterSheet = "CharacterSheet"
    Game = "Game"

logger.debug("***** Importing models/player.py")


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    veils: Mapped[List[str]] = mapped_column(JSONB, default=[])
    lines: Mapped[List[str]] = mapped_column(JSONB, default=[])
    ask_first: Mapped[List[str]] = mapped_column(JSONB, default=[])
    likes: Mapped[List[str]] = mapped_column(JSONB, default=[])
    loves: Mapped[List[str]] = mapped_column(JSONB, default=[])
    games: Mapped[List[Game]] = relationship("Game", back_populates="player")

    def __repr__(self):
        return f"<Player(id={self.id}, name={self.name}, games={self.games})>"
