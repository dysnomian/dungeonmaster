import os
from datetime import datetime
from pathlib import Path
import autogen

from typing_extensions import Annotated

import pandas as pd

logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
print("Logging session ID: " + str(logging_session_id))

chat_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + " Building Creation Chat"
workdir_path = os.path.join(os.getcwd(), "paper")
os.makedirs(workdir_path, exist_ok=True)

docs_dir_path = os.path.join(os.getcwd(), "paper", chat_name + " Docs")
os.makedirs(docs_dir_path, exist_ok=True)

transcript_path = os.path.join(workdir_path, datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_chat_transcript.md")
with open(transcript_path, "w", encoding="utf-8") as file:
    file.write("# Chat Transcript\n\n-------------------\n\n\n")

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")
# beefy_config_list = autogen.config_list_from_json(env_or_file="BIG_OAI_CONFIG_LIST")

general_llm_config = {
    "seed": 45, 
    "temperature": 0.2,
    "config_list": config_list,
    "timeout": 120,
}

# beefy_llm_config = {
#     "seed": 45, 
#     "config_list": beefy_config_list,
#     "temperature": 1,
#     "timeout": 120
# }

def termination_msg(x):
    """
    Check if the message is a termination message.
    """
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()


# humans
user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message="""
    A human admin. Interact with the designer, architect, building planner, software planner, software engineer, code reviewer, and executor.
    """,
    code_execution_config=False,
)

executor = autogen.UserProxyAgent(
    name="Executor",
    human_input_mode="ALWAYS",
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
    system_message="Executor. Execute code and provide the output to the user."
)

# robots

stenographer = autogen.AssistantAgent(
    name="Stenographer",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    code_execution_config={"last_n_messages": 5, "work_dir": workdir_path},
    human_input_mode="NEVER",
    system_message="""
    You are the stenographer. You listen to all messages sent by the user and all other agents, regardless of who they are speaking to, and use the append_message function to append the body of every message to the chat transcript. This is your only job. You do not need to respond to any messages other than the user.
    """
)

@stenographer.register_for_execution()
@stenographer.register_for_llm(
    name="append_message",
    description="Update the transcript file to append the new message and denote the speaker.",
)
def append_message(
    message: Annotated[str, "The message to record."],
    speaker: Annotated[str, "The speaker of the message."],
) -> str:
    """
    Append the message to the transcript file.
    """
    print("Appending message to transcript file.")
    try:
        with open(transcript_path, "a", encoding="utf-8") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            message = timestamp + "\n\n**" + speaker + ":** " + message + "\n\n\n-------------------\n\n\n"
            file.write(message)
        return "The message was appended to " + transcript_path
    except FileNotFoundError:
        return "The transcript file `" + transcript_path + "` was not found."

software_planner = autogen.AssistantAgent(
    name="SoftwarePlanner",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are the software planner. When code is requested to solve a problem, plan the code for the engineer and code reviewer. Describe the task and the expected outcome. Specify requirements. When the code meets the requirements, approve it. 

    When you are given the **Room Connectivity Plan** by the architect, come up with a plan for software to parse it and convert it into a graph data structure. The graph should have nodes for each room and entrance and edges for each connection between rooms. The graph should be able to represent the building's layout and the connections between rooms. When the software is ready, approve it.
    """
)

software_engineer = autogen.AssistantAgent(
    name="SoftwareEngineer",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are a skilled software engineer who is skilled with Python. You write reusable code and flexible scripts. Draft code according to the plan given by the planner. Integrate revisions from the code reviewer. When the code reviewer and planner have approved, send the code to the executor. When the code is executed, if the results are not as expected, return the code to the software engineer for revisions. If they are as expected, submit the output to the architect as a **Proposed Room Graph**.
    """
)

code_reviewer = autogen.AssistantAgent(
    name="CodeReviewer",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are an experienced code reviewer who is skilled with Python. Review the code written by the software engineer. You consider safety, reusability, readability, and purpose. Consider the software planner's requirements. Make suggestions for improvement. When the code is ready, approve it.
    """
)

architect = autogen.AssistantAgent(
    name="Architect",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are a skilled architect. Given an **Expanded List of Requirements** by the building planner and the **Aesthetic Guidelines** by the designer, create a **Preliminary Room List** draft that complies with both. Use the **Building History** document for inspiration.
    
    Submit a draft of the **Preliminary Room List** to the designer and building planner for feedback. Accept feedback from the designer to ensure the **Aesthetic Guidelines** are met. Accept feedback from the building planner to ensure the **Expanded List of Requirements** are met. Create a revised draft of the **Preliminary Room List** that integrates their feedback but fits with your architectural expertise. Submit the revised draft to them for approval.
    
    When they have approved the **Preliminary Room List**, create a **Preliminary Building Plan** that expands on the **Preliminary Room List**.
    
    Consider the space requirements and functionality and decide on an general ground silhouette for the building. Consider area density and geometry and geography of the area. Think about courtyards, light wells, party walls, and other architectural features. Consider the building's relationship to the street and to other buildings. Will the building taper as it goes up, or have relatively straight walls?

    Create a draft **Preliminary Building Plan** that includes:
    - Ground silhouette of the building.
    - List of floors, sections, and outbuildings.
    - List of exterior walls. Name the building's exterior faces based on functionality, type, and direction. (e.g., "North street-facing wall", "South party wall", "Courtyard-facing wall.")
    - List of extrances and exits, noting any special uses. Give them names based on their location and function. (e.g., "Main entrance", "Service entrance", "Emergency exit.")
    - List of vertical elements like multi-story rooms, stairs, dumbwaiters, and chutes. Give them names based on their location and function. (e.g., "Main stairwell", "Dumbwaiter to kitchen.")
    - Finalized **Premiliary Room List**.
    - A description of the intended look of the building from the front/street.
    - 3 ideas for a **Memorable Key Architectural Element** that could be integrated into the building. These could be a room, courtyard, or structure, but they should be memorable and vivid and should reflect the building's purpose and aesthetic.

    Submit the **Preliminary Building Plan** to the designer and the building planner for feedback. Accept feedback from the designer to improve the aesthetics. Accept feedback from the building planner to ensure the **Expanded List of Requirements** are met. If necessary, create a revised draft of the **Preliminary Building Plan** that integrates their feedback and fits with your architectural expertise. Submit the revised draft to them for approval.

    When the **Preliminary Building Plan** is approved, create a **Room Connectivity Plan**. Start with the **Finalized Preliminary Room List**.
    1) If it's not split into floors, sections, or outbuildings already, do so now.
    2) Go through it and ensure that it is complete and each room has its own row on the list and a unique name.
    3) For vertical elements like staircases, give them an entry and a name for each floor they're on (for example, "Main stairwell" becomes "Main stairwell landing, first floor" and "Main stairwell landing, second floor").
    4) Add an entry on the list for each entrance.
    5) If there are any significant outdoor elements like courtyards, gardens, or yards, add an entry for each of them. Add an entry for "Street", "Outside", or whatever is appropriate for the building's exterior outside of its respective entrances.
    6) For each entry, list the following information:
        - List the elements it needs to be close to, or connected to
        - List its light and ventilation requirements, whether those could be fulfilled by a small window, large window, skylight, or light well, or whether lamps alone might be sufficient
        - If it's a room or enclosed area, estimate the area of the room. Provide an upper and lower bound and an ideal size.
        - Whether the room requires an external-facing wall, needs to be an interior room, or is flexible. If it needs an external-facing wall, say whether it needs to be on a specific wall or not.

    Once you have a draft of the **Room Connectivity Plan**, submit it to the designer and the building planner for feedback. Accept feedback from the designer to improve the aesthetics. Accept feedback from the building planner to ensure the **Expanded List of Requirements** are met. If necessary, create a revised draft of the **Room Connectivity Plan** that integrates their feedback and fits with your architectural expertise. Submit the revised draft to them for approval. Once they have approved the **Room Connectivity Plan**, submit it to software planner.

    When you have received the data back from the software planner, review it to ensure that it is consistent with the **Room Connectivity Plan**. If it is not, request changes. If it is, approve it and request a graph visualization of the data with all nodes and edges labeled.

    Create a new **Updated Building Plan** that integrates all the connections in the building graph. Look over it to ensure that it makes sense from an archtectural standpoint, then offer it to the user for review and approval. If it is approved, submit it to the designer and building planner for final approval. If it is not approved, make changes as necessary and resubmit it for approval.
    """,
)

building_planner = autogen.AssistantAgent(
    name="BuildingPlanner",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are a building planner. Based on the building type and any specifications given by the user, you create an **Expanded List of Requirements** for the building.
    
    Use this process to build out **Expanded List of Requirements**:

    1) Think through the practical requirements of a building like that and how it might fulfill them. Consider first whether these needs apply at all, whether they would be provided by the building or the surroundings, and to what degree they apply. For example, a bank may need to give significant thought to robbery, but a coal depot might not. Consider:
    - Number of occupants. Consider how many people might work, live in, or visit the building at once.
	- Storage. Consider what kinds of materials, tools, and products this building might need to store.
	- Special doors, windows, or chutes for things like large cargo, coal or grain, feed, building materials, wagons.
	- Special entrance areas like reception, cloakrooms, mudrooms.
	- Water supply, garbage, and sewage.
	- Food and fuel requirements and storage.
	- Proximity to other resources not on site.
	- Geographic necessities. For example, a shipwright's workshop will need to be adjacent to water.
	- Transportation for people, cargo, any products, and waste. Consider whether this might include vehicles or animals. (For example, many buildings will require beasts of burden for transporting heavy cargo, but only porters and teamsters will be likely to keep them on-site.)
	- Security needs. Consider theft, robbery, outright attack from hostiles, espionage. 
	- Safety considerations such as fire prevention. Some buildings have unusual safety considerations like hazardous chemical handling and storage.
	- Outdoor spaces like yards, gardens.
	- Sanitation needs like garbage, baths, or privies.
	- Building materials would it use to meet these needs.

    2) Consider constraints the building might have. Does it have hard geographical requirements, such as water access for a shipwright's workshop? If it's in a dense urban area, it might have to make careful use of space and have more floors and no outbuildings.

    3) Figure out how the building might fulfill its needs given its limitations. what sections it might have and how many floors it would have. Make a list of the rooms likely to be in the building. List which rooms would be likely to be on which floors or in which outbuildings, if applicable. Include any stairs, hallways, storage areas, and entrances, and entryways. Think through this step-by-step.
    
    Review the **Preliminary Room List** draft from the architect. Ensure that it meets the **Expanded List of Requirements**. If it does, approve it. If it does not, suggest changes to the architect.

    """
)

# user requirements ->
# building planner: expanded list of requirements ->
# lore expert: (user requirements, expanded requirements) **Building History** ->
# designer: (expanded requirements, building history) aesthetic guidelines ->
# architect: (expanded requirements, aesthetic guidelines) preliminary room list ->
# designer: (expanded list of requirements) aesthetic design ->
designer = autogen.AssistantAgent(
    name="Designer",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are a creative building designer. When provided with the finalized **Expanded List of Requirements** and finalized **Building History** by the building planner, use them to come up with succinct **Aesthetic Guidelines** document for the building. In this document, describe the aesthetic. What specific materials does it use? Does it have thematic colors? Is it functional and practical or decorative? Are there windows, and if so, are they practical, or decorative? Are there plants, curtains, rugs, stonework? Is it neat and tidy or cluttered? Is it well-maintained or run down? Is it minimalist? Is it grand and imposing, or cozy and welcoming? Does it stand out from its surroundings or blend in?

    Given the setting and location, decide on the resources likely to be available for the building. Consider money available for building and maintenance, the degree of technological and/or magical advancement, and any local resources. Has it been through rough times, come from humble beginnings, or had a golden age in the past? If the building is likely to be old, it might have had many years to accumulate improvements, or it might be beginning to fall apart. Is it well-loved or neglected?

    Be creative and make it memorable and vivid! Submit the draft **Aesthetic Guidelines** to the lore expert for approval. When it is approved, submit it to the architect.

    When given a **Preliminary Room List** draft by the architect, provide feedback to the architect to ensure the **Aesthetic Guidelines** are met. When the **Preliminary Room List** draft meets the **Aesthetic Guidelines**, approve it.
    
    When the architect presents a draft of the **Preliminary Building Plan**, provide feedback to ensure that the **Aesthetic Guidelines** are met. Review the **Key Architectural Element** ideas and provide feedback. If one or more is ideal for the building and its aesthetic, state which ones and approve the **Preliminiary Building Plan.** If none are ideal, suggest a new one, or suggest a way to integrate one into the existing room list. Either way, be creative and make it memorable and vivid! When you and the architect have agreed on an **Key Architectural Element** and agree on the draft, approve the **Preliminary Building Plan**.
    """
)

@architect.register_for_execution()
@architect.register_for_llm(
    name="create_planning_document",
    description="Create a planning document for the building to share with other agents."
)
@building_planner.register_for_execution()
@building_planner.register_for_llm(
    name="create_planning_document",
    description="Create a planning document for the building to share with other agents."
)
def create_planning_document(
    name: Annotated[str, "The name of the planning document."],
    body: Annotated[str, "The body of the planning document."],
    version: Annotated[str, "The version of the planning document."]
) -> str:
    """
    Create a planning document for the building to share with other agents.
    """
    print("Creating planning document.")
    try:
        with open(os.path.join(docs_dir_path, name + "_" + version + ".md"), "w", encoding="utf-8") as file:
            file.write(body)
        return "The planning document was created."
    except FileNotFoundError:
        return "The planning document could not be created."

@architect.register_for_execution()
@architect.register_for_llm(
    name="read_planning_document",
    description="Read a planning document for the building."
)
def read_planning_document(
    name: Annotated[str, "The name of the planning document."]
) -> str:
    """
    Read a planning document for the building.
    """
    print("Reading planning document.")
    try:
        with open(os.path.join(docs_dir_path, name), "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "The planning document could not be found."

@architect.register_for_execution()
@architect.register_for_llm(
    name="list_planning_documents",
    description="List all planning documents for the building."
)
def list_planning_documents() -> str:
    """
    List all planning documents for the building.
    """
    print("Listing planning documents.")
    files = os.listdir(docs_dir_path)
    return "\n".join(files)


lore_expert = autogen.AssistantAgent(
    name="LoreExpert",
    is_termination_msg=termination_msg,
    llm_config=general_llm_config,
    system_message="""
    You are a lore expert well-versed in the lore of the Forgotten Realms setting.

    When presented with the draft **Expanded List of Requirements** by the building planner, review it to ensure that it is consistent with the lore of the Forgotten Realms setting. If it is not, suggest revisions to make it more consistent with the lore. When the **Expanded List of Requirements** is consistent with the lore, approve it.

    Use the user's requirements and the finalized version of the **Expanded List of Requirements** to come up with a **Building History** document. Consider the setting and location. Has it been through rough times, come from humble beginnings, or had a golden age in the past? If the building is likely to be old, it might have had many years to accumulate improvements, or it might be beginning to fall apart. Is it well-loved or neglected? Be creative and make it memorable and vivid! Submit the **Building History** to the building planner.
    
    You provide feedback to the designer and the building planner to ensure that the **Expanded List of Requirements** and **Aesthetic Guidelines** are consistent with the lore of the Forgotten Realms setting. Suggest revisions to make the **Expanded List of Requirements** and **Aesthetic Guidelines** more consistent with the lore and integrate more lore elements into the building design. When they are ready, approve them. Do not talk with any other agents.
    """
)

# start the "group chat" between agents and humans
groupchat = autogen.GroupChat(
    agents=[
        user_proxy,
        stenographer,
        # lore_expert,
        # software_planner,
        # software_engineer,
        # code_reviewer,
        # architect,
        building_planner,
        # designer,
        # executor
    ],
    messages=[],
    max_round=50,
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=general_llm_config
)

# Start the Chat!
user_proxy.initiate_chat(
    manager,
    message="""
    Building Planner and Lore Expert: design me a small, broken-down hovel in the woods for a DND campaign.
    """,
)

# to followup of the previous question, use:
# user_proxy.send(
#     recipient=assistant,
#     message="""your followup response here""",
# )

autogen.runtime_logging.stop()