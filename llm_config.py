"Default configuration for LLM agents."

from autogen import config_list_from_json

LLM_CONFIG = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

DEFAULT_AGENT_CONFIG = {
    "seed": 42,
    "temperature": 0.5,
    "config_list": LLM_CONFIG,
    "timeout": 120,
}


def termination_msg(x):
    """
    Check if the message is a termination message.
    """
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
