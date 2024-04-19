import autogen
from __old_stuff.character_sheet_team.config import agent_config, termination_msg

rules_expert = autogen.AssistantAgent(
    name="RulesExpert",
    is_termination_msg=termination_msg,
    llm_config=agent_config,
    system_message="""
    You are a rules expert on the rules of DND 5e. You are brief and factual and answer questions about the rules. You review plans suggested by the gamemaster and explain which rules are relevant to the plan. You evaluate whether changes to a proposed character preserve the intended meaning.
    """,
)
