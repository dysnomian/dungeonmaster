from typing import Annotated

import autogen

from agents.config import agent_config, termination_msg
from agents.stenographer import stenographer
from dice_roller import DiceRoller
from transcript import Transcript
from game_state_manager import GameStateManager
from state_manager_agent import StateManagerAgent

# we can select a game later on. For now, we'll just use the default game state
game_state = GameStateManager("game_1.game_state.json")
transcript = Transcript(game_state)

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")

general_llm_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0.2,
    "config_list": config_list,
    "timeout": 120,
}

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
    description="Read the game meta properties from a file",
    api_style="tool",
)
def fetch_game_meta() -> Annotated[dict, "game_meta"]:
    return game_state.meta()


@gamemaster.register_for_execution()
@gamemaster.register_for_llm(
    description="Read the game story from a file",
    api_style="tool",
)
def fetch_story() -> Annotated[dict, "story"]:
    return game_state.story()


@gamemaster.register_for_execution()
@gamemaster.register_for_llm(
    description="Read the campaign from a file",
    api_style="tool",
)
def fetch_campaign() -> Annotated[dict, "story"]:
    return game_state.campaign()


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
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=general_llm_config,
)

# Start the Chat!
user_proxy.initiate_chat(
    manager,
    message="""
    Please start a game from a game state JSON file. Use the game_1.game_state.json file to start.
    """,
)

# to followup of the previous question, use:
# user_proxy.send(
#     recipient=assistant,
#     message="""your followup response here""",
# )
