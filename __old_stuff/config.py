import autogen

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST")

agent_config = {
    "seed": 42,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

def termination_msg(x):
    """
    Check if the message is a termination message.
    """
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
