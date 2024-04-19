import autogen
from __old_stuff.character_sheet_team.config import agent_config, termination_msg
from agents.stenographer import stenographer

from agents.character_sheet_team.team import (
    team_members as character_sheet_team_members,
)
from agents.character_sheet_team.team import character_sheet_team_speaker_transitions

from agents.character_sheet_team.character_sheet_leader import character_sheet_leader


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
    A human admin. Interact with the character expert, rules expert, and lore
    expert to help shape the character sheet.
    """,
    code_execution_config=False,
)

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

agents = [
    user_proxy,
    supervisor,
    stenographer,
    rules_expert,
].append(character_sheet_team_members)

allowed_speaker_transitions_dict = {
    user_proxy: [supervisor],
    supervisor: [user_proxy, stenographer, character_sheet_leader],
    stenographer: [user_proxy],
}.update(character_sheet_team_speaker_transitions)

visualize_speaker_transitions_dict(allowed_speaker_transitions_dict, agents)
plt.savefig("speaker_transitions.png")

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
    Create a JSON representation of the character Marshmallow described in her
    character file. Compare with the other character sheets
    to ensure consistency. When done, write the new character sheet JSON to
    tmp/marshmallow_generated.json.
    """,
)

# to followup of the previous question, use:
# user_proxy.send(
#     recipient=assistant,
#     message="""your followup response here""",
# )
