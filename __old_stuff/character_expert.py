import os
from typing import Annotated

import autogen
from __old_stuff.character_sheet_team.config import agent_config, termination_msg

character_expert = autogen.AssistantAgent(
    name="CharacterExpert",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    code_execution_config={"last_n_messages": 2, "work_dir": "json_data/characters"},
    system_message="""
    You are an expert on a given character. You search the characters directory
    for a file that contains information about them.

    If this file cannot be found, explain the error and say "TERMINATE" to end the conversation.

    You answer questions about the character.

    You review the character sheet JSON proposed by the character sheet JSON composer. You ensure it is accurate and suggest changes to the proposed JSON files to keep it faithful to character information you have and ensure it is comprehensive.

    When the character sheet JSON composer proposes a draft that is accurate and comprehensive, you approve it. If it is not, you suggest revisions to the file and approve it when it is ready. You go into detail with the changes that need to be made to the JSON file to make it accurate and comprehensive.
    """,
)


@character_expert.register_for_execution()
@character_expert.register_for_llm(
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


@character_expert.register_for_execution()
@character_expert.register_for_llm(
    name="read_character_info", description="Read in the raw character info."
)
def read_character_info(
    filename: Annotated[str, "The filename of the character info."],
) -> str:
    """
    Reads the character info from a file.
    """
    try:
        with open("json_data/characters/" + filename, "r", encoding="utf-8") as file:
            character_info = file.read()
        return character_info
    except FileNotFoundError:
        return "The character info file was not found."
