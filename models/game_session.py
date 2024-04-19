import json

from typing import Any, List

from models.base import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP
from sqlalchemy.sql.functions import now

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.game import Game


dialogue_default = json.dumps(
    {"currently_in_dialogue": False, "speakers": [], "current_speaker": None}
)
combat_default = json.dumps(
    {
        "currently_in_combat": False,
        "combatants": [],
        "current_turn": None,
        "round": 0,
        "initiative_order": [],
    }
)


class GameSession(Base):
    def __init__(self, **kw: Any):
        super().__init__(**kw)

    __tablename__ = "game_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    game: Mapped["Game"] = relationship("Game", back_populates="game_sessions")
    summary: Mapped[str] = mapped_column(String, default="")
    current_location: Mapped[str] = mapped_column(String, default="")
    current_time: Mapped[str] = mapped_column(String, default="")
    player_actions_taken: Mapped[int] = mapped_column(Integer, default=0)
    created_at = mapped_column(TIMESTAMP, default=now())
    completed_at = mapped_column(TIMESTAMP, nullable=True)
    dialogue: Mapped[List[Any]] = mapped_column(JSONB, default=dialogue_default)
    combat: Mapped[List[Any]] = mapped_column(JSONB, default=combat_default)
