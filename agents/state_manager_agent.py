"""
The state manager agent is responsible for managing the game state. It can update the game state, save it, roll it back, and validate it.
"""

from typing import Annotated, List
from sqlalchemy import select
from db import session

from agent_superclass import AgentSuperclass
from models.game import Game


def read_game_state(
    game_id: Annotated[int, "The id of the game to manage."],
) -> object:
    stmt = select("Game").where("Game.id == game_id")
    game = session.execute(stmt).scalars().first()
    return game


class StateManagerAgent(AgentSuperclass):

    @property
    def name(self) -> str:
        return "StateManager"

    @property
    def description(self) -> str:
        return "Manages the state of the game, including details about the campaign, story, and player characters."

    @property
    def system_message(self) -> str:
        return """
        You are the state manager. You are responsible for managing the game state. You can update the game state and save it to the database. You can also load the game state from a file. You can also validate the game state against a schema and save it to a file. You can also read the game state from a file.

        Every time something happens in the game that should change the game state, update it and save it to the database. If the game state can't be loaded, saved, or read for any reason, explain what happened in as much detail as you can and say "TERMINATE" to end the conversation.
        """

    @property
    def code_execution_config(self) -> dict:
        return {"last_n_messages": 10, "work_dir": "json_data/games/"}

    @property
    def functions(self) -> List[dict]:
        return [
            {
                "name": "read_game_state",
                "description": "Read the game state from the database",
                "callable_function": read_game_state,
            }
        ]
