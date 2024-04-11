import json
from typing_extensions import Annotated

import autogen
from agents.config import agent_config, termination_msg

cs_json_composer = autogen.AssistantAgent(
    name="CharacterSheetJsonComposer",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    system_message="""
    You are a character sheet JSON composer. You take character information given by the character expert and and compose it into a JSON representation.

    You are rigid and follow instructions from the character expert, the rules expert, and the character sheet schema validator.

    Once it is approved, present it to the character sheet team leader to be written to the file.
    """,
)
