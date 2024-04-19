from typing import Annotated, List
from sqlalchemy import select
from db import session

from agent_superclass import AgentSuperclass
from models import Campaign, Game, Player

STARTING_GAME_ID = 1


def get_game_context(
    game_id: Annotated[int, "The id of the game to manage."],
    player_id: Annotated[int, "The id of the player to manage."],
) -> object:
    stmt = select(Game.game_length__sessions, Game.tone, Game.setting).where(
        Game.id == game_id
    )
    game = session.execute(stmt).scalars().first()
    return game


class PlotWriterAgent(AgentSuperclass):

    @property
    def name(self) -> str:
        return "PlotWriter"

    @property
    def description(self) -> str:
        return "Given game context, player context, and game config, generates an outline of the plot and updates it as the game progresses."

    @property
    def system_message(self) -> str:
        return """
        You are the plot writer. You are responsible for generating the plot of the game and updating it as the game progresses.

        Given the game length, session length, difficulty, tone, players' veils and lines (if any), and the player's character sheets, you will generate an outline of the plot.

        When generating a plot, you come up with a series of events that will happen in the game. These events should be interesting, challenging, and engaging for the players. They should also be tailored to the players' character backstory and the game's setting, if provided.

        Come up with an engaging and intriguing premise for the game. This could be a mystery, a heist, a political intrigue, or anything else that you think would be fun for the players. Write a brief "elevator pitch" summary that intrigues the players and sets the tone for the game and conceals the plot twists and surprises.

        Given a number of sessions, come up with a goal for each session. This could be a major plot point, a character development moment, or a challenge for the players to overcome. Make sure that each session has a clear goal and moves the plot forward. Come up with a series of steps the players could take to achieve that goal, and a series of obstacles they might face along the way.
        """

    @property
    def code_execution_config(self) -> dict:
        return {"last_n_messages": 10, "work_dir": "json_data/games/"}

    @property
    def functions(self) -> List[dict]:
        return [
            {
                "name": "get_game_context",
                "description": "Read the game context from the database.",
                "callable_function": get_game_context,
            }
        ]
