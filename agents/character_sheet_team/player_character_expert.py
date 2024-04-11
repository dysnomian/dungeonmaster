import os
from typing import Annotated

import autogen
from agents.config import agent_config, termination_msg

player_character_expert = autogen.AssistantAgent(
    name="PlayerCharacterExpert",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "json_data/characters"
        },
    system_message="""
    You are an expert on the player character. You search the characters directory for files that contain information about the player character.

    If no files about them can be found, explain the error and say "TERMINATE" to end the conversation.

    When the character sheet team leader approves a new draft of the character sheet JSON, you read it and update the character information you have.

    You answer questions about the character.

    You review the character sheet JSON proposed by the character sheet JSON composer. You ensure it is accurate and suggest changes to the proposed JSON files to keep it faithful to character information you have and ensure it is comprehensive.

    When the character sheet JSON composer proposes a draft that is accurate and comprehensive, you approve it. If it is not, you withhold approval, suggest revisions to the file, and approve it when it is ready. You go into detail with the changes that need to be made to the JSON file to make it accurate and comprehensive.
    """,
)

@player_character_expert.register_for_execution()
@player_character_expert.register_for_llm(
    name="list_character_files", description="List the character files."
)
def list_character_files() -> str:
    """
    Lists the character files in the characters directory.
    """
    try:
        character_files = os.listdir("json_data/characters")
        return character_files
    except FileNotFoundError:
        return "The characters directory was not found."

@player_character_expert.register_for_execution()
@player_character_expert.register_for_llm(
    name="read_character_info", description="Read in the raw character info."
)
def read_character_info(
    filename: Annotated[str, "The filename of the character info."]
) -> str:
    """
    Reads the character info from a file.
    """
    try:
        with open("json_data/characters/" + filename,
                  "r", encoding="utf-8") as file:
            character_info = file.read()
        return character_info
    except FileNotFoundError:
        return "The character info file was not found."
