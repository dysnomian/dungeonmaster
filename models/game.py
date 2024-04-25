from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from utils.logging import logger
from models.base import Base

if TYPE_CHECKING:
    from models.player import Player
    from models.campaign import Campaign
    from models.game_session import GameSession
    from models.campaign import Campaign

logger.debug("***** Importing models/game.py")


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    rules_set = mapped_column(String, default="D&D 5e")
    game_length__sessions = mapped_column(Integer, nullable=True)
    session_length__responses = mapped_column(Integer, nullable=True)
    tone = mapped_column(String, nullable=True)
    difficulty = mapped_column(String, default="normal")
    setting = mapped_column(String)
    npc_death_allowed = mapped_column(Boolean, default=True)
    pc_death_allowed = mapped_column(Boolean, default=True)
    rule_modifications = mapped_column(JSONB, default={})
    player_id: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    player: Mapped["Player"] = relationship("Player", back_populates="games")
    game_sessions: Mapped["GameSession"] = relationship("GameSession", back_populates="game")
    campaign: Mapped["Campaign"] = relationship(back_populates="game")

    def __repr__(self):
        return f"<Game(id={self.id}, name={self.name} rules_set={self.rules_set}), game_length__sessions={self.game_length__sessions}, session_length__responses={self.session_length__responses}, tone={self.tone}, difficulty={self.difficulty}, setting={self.setting}, npc_death_allowed={self.npc_death_allowed}, pc_death_allowed={self.pc_death_allowed}, player={self.player})>"
