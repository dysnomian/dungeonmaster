import os
import json
from typing_extensions import Annotated
import autogen
import jsonschema

print("Working directory: ", os.getcwd())

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")

general_llm_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0.2,
    "config_list": config_list,
    "timeout": 120,
}

agent_config = {
    "seed": 42,  # change the seed for different trials
    "temperature": 0.2,
    "config_list": config_list,
    "timeout": 120,
}


def termination_msg(x):
    """
    Check if the message is a termination message.
    """
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()


# humans
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="""
    A human admin. Interact with the character expert, rules expert, and lore 
    expert to help shape the character sheet.
    """,
    code_execution_config=False,
)

executor = autogen.UserProxyAgent(
    name="Executor",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
    system_message="Executor. Execute the code written by the engineer and report the result.",
)

# robots
stenographer = autogen.AssistantAgent(
    name="Stenographer",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    code_execution_config={"last_n_messages": 10, "work_dir": "transcripts"},
    # human_input_mode="NEVER",
    system_message="""
    You are the group stenographer. You record the conversation. You start a Markdown transcript file
    in the transcripts directory as soon as the conversation begins,
    using an informative filename. You compose a YAML frontmatter section 
    at the start of the file with date and time metadata, as well as the names of the participants.
    When new messages are sent, you append them to the transcript file. You include the name of the speaker
    and the timestamp. You do not participate in the conversation.

    If there is an error creating the transcript file, explain the error and say "TERMINATE" to end the conversation.
    """,
)


@user_proxy.register_for_execution()
@stenographer.register_for_llm(
    name="start_transcript_file", description="Start the transcript file."
)
def start_transcript_file(
    filename: Annotated[str, "The filename of the transcript in the transcripts directory."],
    metadata: Annotated[str, "The metadata of the transcript in YAML format."],
) -> str:
    """
    Start the transcript file with the metadata.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(metadata + "\n---\n\n")
            return "The transcript file `" + filename + "` was created in the transcripts directory."
    except FileNotFoundError as e:
        return "The transcript file was not found: " + str(e)
    except PermissionError as e:
        return "Permission denied to write to the transcript file: " + str(e)


@user_proxy.register_for_execution()
@stenographer.register_for_llm(
    name="append_message",
    description="Update the transcript file to append the new message.",
)
def append_message(
    filename: Annotated[str, "The filename of the transcript in the transcripts directory."],
    message: Annotated[str, "The message to record."],
) -> str:
    """
    Append the message to the transcript file.
    """
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(message + "\n\n\n-------------------\n\n\n")
        return "The message was appended to the transcript file at `" + filename + "` in the transcripts directory."
    except FileNotFoundError:
        return "The transcript file at `" + filename + "` was not found."


rules_expert = autogen.AssistantAgent(
    name="RulesExpert",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    system_message="""
    You are a rules expert on the rules of DND 5e. You are brief and factual and
    answer questions about the rules. You review plans suggested by the gamemaster 
    and explain which rules are relevant to the plan. You evaluate whether changes to a 
    proposed character preserve the intended meaning.
    """
)

lore_expert = autogen.AssistantAgent(
    name="LoreExpert",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    system_message="""
    You are a lore expert on the lore of Forgotten Realms. You are brief and factual and
    answer questions about the lore. You review ideas suggested by the storymaster
    and contribute to the story with your knowledge of the lore.
    """,
)

character_expert = autogen.AssistantAgent(
    name="CharacterExpert",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    code_execution_config={"last_n_messages": 2, "work_dir": "./json_data/characters"},
    system_message="""
    You are an expert on a given character. You search the characters directory for a file that contains 
    information about them. 

    If this file cannot be found, explain the error and say "TERMINATE" to end the conversation.

    You then answer questions about it and suggest changes to the JSON schema to keep it faithful to
    character information you have. You work with the rules expert and the json composer to find ways
    to represent the character in JSON. If there is an error reading the file, explain what the error is and how
    to fix it. Go into detail.
    """,
)

@user_proxy.register_for_execution()
@character_expert.register_for_llm(
    name="list_character_files", description="List the character files."
)
def list_character_files() -> str:
    """
    Lists the character files in the characters directory.
    """
    try:
        character_files = os.listdir("./json_data/characters")
        return character_files
    except FileNotFoundError:
        return "The characters directory was not found."

@user_proxy.register_for_execution()
@character_expert.register_for_llm(
    name="read_character_info", description="Read in the raw character info."
)
def read_character_info(
    filename: Annotated[str, "The filename of the character info."]
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


schema_validator = autogen.AssistantAgent(
    name="SchemaValidator",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    code_execution_config={"last_n_messages": 2, "work_dir": "json_data/schemas"},
    system_message="""
    You are a JSON schema validator. You review any proposed character sheet JSON
      and validate it against the expected schema.

    If it is valid, you approve it. If it is invalid, you suggest revisions to the file and approve it when it is ready.
    """,
)


@user_proxy.register_for_execution()
@schema_validator.register_for_llm(
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
    except FileNotFoundError:
        return "The character sheet schema file was not found."


@user_proxy.register_for_execution()
@schema_validator.register_for_llm(
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


json_composer = autogen.AssistantAgent(
    name="JsonComposer",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    system_message="""
    You are a JSON composer. You take character information given by the character expert and
    and compose it into JSON. 

    You are rigid and follow instructions from the user, the character expert, the rules expert, and the schema validator.

    You follow feedback from the character expert, rules expert, the schema validator, and the lore expert
    to revise the JSON file until it is approved by all of them.

    Once it is approved, present it to the admin. If the admin asks for revisions, make them.
    """,
)


@user_proxy.register_for_execution()
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

supervisor = autogen.AssistantAgent(
    name="Supervisor",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    system_message="""
    You are the supervisor. You oversee the conversation and ensure that the conversation
    is productive and on track. You provide feedback to the group and ensure that the
    conversation is moving in the right direction. You can ask for clarification or
    ask the group to move on to the next step. You ensure that each agent is focusing on
    their assigned task.
    """,
)

# start the "group chat" between agents and humans
groupchat = autogen.GroupChat(
    agents=[
        user_proxy,
        supervisor,
        character_expert,
        # lore_expert,
        rules_expert,
        json_composer,
        schema_validator,
        stenographer,
    ],
    messages=[],
    max_round=50,
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=general_llm_config)

# Start the Chat!
user_proxy.initiate_chat(
    manager,
    message="""
    Create a JSON representation of the character Marshmallow described in her 
    character file. Compare with the other character sheets
    to ensure consistency. When done, write the new character sheet JSON to 
    a file called marshmallow.json.
    """,
)

# to followup of the previous question, use:
# user_proxy.send(
#     recipient=assistant,
#     message="""your followup response here""",
# )
