import autogen
from agents.config import agent_config, termination_msg

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
