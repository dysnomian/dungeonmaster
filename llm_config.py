"Default configuration for LLM agents."

import os

from autogen import config_list_from_json

USE_LOCAL_LLM = os.getenv("USE_LOCAL_LLM", "False").lower() == "true"

filter_dict = {}

if USE_LOCAL_LLM:
    filter_dict = {"tags": ["local"]}

LLM_CONFIG = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

DEFAULT_AGENT_CONFIG = {
    "cache_seed": None,
    "temperature": 0.5,
    "config_list": LLM_CONFIG,
    "timeout": 120,
}

LOCAL_AGENT_CONFIG = {
    "cache_seed": None,
    "temperature": 0.5,
    "config_list": [
        {
            "name": "Llama3",
            "model": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
            "api_key": "lm-studio",
        }
    ],
    "timeout": 120,
}


def termination_msg(x):
    """
    Check if the message is a termination message.
    """
    return isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()
