import json
from typing_extensions import Annotated

import autogen
from agents.config import agent_config, termination_msg

json_composer = autogen.AssistantAgent(
    name="JsonComposer",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    system_message="""
    You are a JSON composer. You take character information given by the character expert and and compose it into JSON.

    You are rigid and follow instructions from the user, the character expert, the rules expert, and the schema validator.

    You follow feedback from the character expert, rules expert, the schema validator, and the lore expert to revise the JSON file until it is approved by all of them.

    Once it is approved, present it to the admin. If the admin asks for revisions, make them.
    """,
)


@json_composer.register_for_execution()
@json_composer.register_for_llm(
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
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(character_sheet_json, file, indent=4)
    return "The character sheet JSON was written to the file."
