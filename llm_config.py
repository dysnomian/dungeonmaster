"Default configuration for LLM agents."
from autogen import config_list_from_json

DEFAULT_LLM_CONFIG = {
    "seed": 42,
    "temperature": 0.5,
    "config_list": config_list_from_json(env_or_file="OAI_CONFIG_LIST"),
    "timeout": 120,
}
