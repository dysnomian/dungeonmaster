from typing import Annotated, Union, List, Any

import autogen

# import Sequence
from llm_config import LLM_CONFIG, termination_msg
from __old_stuff.character_sheet_team.config import agent_config, termination_msg
from agents.stenographer import stenographer
from agents.dice_roller import DiceRoller
from transcript import Transcript
from db import engine

from state_manager_agent import StateManagerAgent
from sqlalchemy.sql import select

from db import session as sesh
from models.game import Game
from models.campaign import Campaign
from models.game_session import GameSession

from sqlalchemy.orm import sessionmaker

# we can select a game later on. For now, we'll just use the default game state
STARTING_GAME_ID = 1

transcript = Transcript(STARTING_GAME_ID)

# humans
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="""
    A human admin.
    """,
)

gamemaster = autogen.AssistantAgent(
    name="GameMaster",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 10, "work_dir": "json_data/games/"},
    system_message="""
    You are a GameMaster. You are responsible for describing the world and progressing the game. You answer questions about the world and provide information about the setting. You can also introduce new characters and plot points. You ask the user, "What would you like to do next?" to prompt them to take action.

    When something in the game state needs to change, you can ask the state manager to do it.
    """,
)


@gamemaster.register_for_execution()
@gamemaster.register_for_llm(
    description="Read the game model from the database",
    api_style="tool",
)
def game() -> Annotated[Union[Game, object], "game model"]:
    """Read the game model from the database"""
    stmt = select(Game).where(Game.id == STARTING_GAME_ID)
    return sesh.execute(stmt).scalars().first()


@gamemaster.register_for_execution()
@gamemaster.register_for_llm(
    description="Read the campaign from the database",
    api_style="tool",
)
def campaign() -> Annotated[Union[Campaign, object], "campaign"]:
    """Read the game's campaign from the database"""
    stmt = select(Campaign).where(Campaign.game_id == STARTING_GAME_ID)
    return sesh.execute(stmt).scalars().first()


@gamemaster.register_for_execution()
@gamemaster.register_for_llm(
    description="Read the campaign story from the database",
    api_style="tool",
)
def story() -> (
    Annotated[
        Union[dict[str, Any], None], "Campaign story summary, goals, and objectives"
    ]
):
    """Read the game's campaign story from the database"""
    stmt = select(Campaign.story).where(Campaign.game_id == STARTING_GAME_ID)
    return sesh.execute(stmt).scalars().first()


@gamemaster.register_for_execution()
@gamemaster.register_for_llm(
    description="Read the current game session from the database",
    api_style="tool",
)
def current_game_session() -> Annotated[Union[GameSession, None], "game session"]:
    stmt = select(Game).where(Game.id == STARTING_GAME_ID)
    game = sesh.execute(stmt).scalars().first()
    if type(game) == Game:
        return game.current_session()


def append_message(
    message: Annotated[str, "message"],
    sender: Annotated[str, "sender"],
) -> bool:
    return transcript.append_message(message, sender)


dice_roller = DiceRoller({"user_proxy": user_proxy}).agent

state_manager = StateManagerAgent({"user_proxy": user_proxy}).agent

autogen.agentchat.register_function(
    append_message,
    caller=stenographer,
    executor=user_proxy,
    name="append_message",
    description="Append a message to the transcript",
)

agents = [user_proxy, stenographer, gamemaster, dice_roller, state_manager]

# start the "group chat" between agents and humans
groupchat = autogen.GroupChat(
    agents=agents,
    messages=[],
    max_round=20,
    # allowed_or_disallowed_speaker_transitions=allowed_speaker_transitions_dict,
    # speaker_transitions_type="allowed"
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=LLM_CONFIG[0])

# Start the Chat!
user_proxy.initiate_chat(
    manager,
    message="""
    Please recap the story for the current game session.
    """,
)

# to followup of the previous question, use:
# user_proxy.send(
#     recipient=assistant,
#     message="""your followup response here""",
# )
