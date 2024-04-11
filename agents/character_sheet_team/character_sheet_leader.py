import json
from typing import Annotated

import autogen
from agents.config import agent_config, termination_msg

character_sheet_leader = autogen.AssistantAgent(
    name="CharacterSheetLeader",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    system_message="""
    You are the character sheet team leader. You oversee the maintenance of the player's character sheet.

    You ensure that the character sheet JSON is created correctly and that the schema validator approves it before it is completed.

    Once you, the schema validator, and the character expert approve the character sheet JSON, you write it to the file.
    """,
)

@character_sheet_leader.register_for_execution()
@character_sheet_leader.register_for_llm(
    name="write_character_sheet_json",
    description="Write the character sheet JSON from the character information.",
)
def write_character_sheet_json(
    character_sheet_json: Annotated[str, "The character sheet JSON to write."],
    filename: Annotated[str, "The filename to write the character sheet JSON to."],
) -> str:
    """
    Writes the character sheet JSON to a file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(character_sheet_json, file, indent=4)
        return "The character sheet JSON was written to the file."
    except PermissionError as e:
        return "You do not have permission to write to the file: " + str(e)
