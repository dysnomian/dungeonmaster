import json
from typing import Annotated

import autogen
import jsonschema
from agents.config import agent_config, termination_msg

cs_json_validator = autogen.AssistantAgent(
    name="CharacterSheetJSONValidator",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    code_execution_config={"last_n_messages": 2, "work_dir": "json_data/schemas"},
    system_message="""
    You are the character sheet JSON schema validator. You review any proposed character sheet JSON and validate it against the expected schema.

    If it is valid, you approve it. If it is invalid, you suggest revisions to the file and approve it when it is ready.
    """,
)

@cs_json_validator.register_for_execution()
@cs_json_validator.register_for_llm(
    name="read_character_sheet_schema",
    description="Read in the character sheet JSON schema.",
)
def read_character_sheet_schema() -> str:
    """
    Reads the character sheet schema from a file.
    """
    try:
        with open("./json_data/schemas/character_sheet_schema.json", "r", encoding="utf-8") as file:
            character_sheet_schema = json.load(file)
        return character_sheet_schema
    except FileNotFoundError as e:
        return "The character sheet schema file was not found: " + str(e)


@cs_json_validator.register_for_execution()
@cs_json_validator.register_for_llm(
    name="validate_character_sheet_json",
    description="Validates the given character sheet JSON against the character sheet schema and enumerates errors to fix.",
)
def validate_character_sheet_json(
    character_sheet_json: Annotated[dict, "The character sheet JSON to validate."],
    schema: Annotated[dict, "The character sheet JSON schema."],
) -> str:
    """
    Validates the character sheet JSON against the schema and returns the errors.
    """

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(character_sheet_json), key=lambda e: e.path)

    if errors:
        error_messages = []
        for error in errors:
            message = f"Error at {'->'.join(map(str, error.path))}: {error.message}"
            error_messages.append(message)
        detailed_error_message = "\n".join(error_messages)
        return detailed_error_message
    else:
        return "The character sheet is valid."
