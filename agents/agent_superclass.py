"""
This module provides a superclass for creating agent wrappers.
"""

from typing import List, Union, Tuple

from autogen import AssistantAgent, UserProxyAgent, register_function

from llm_config import DEFAULT_AGENT_CONFIG


class AgentSuperclass:
    """
    Inherit from this class to create an agent wrapper that registers functions.

    The config must contain the following:
    - name: str. The name of the agent in the conversation.
    - llm_config: dict. The config for the LLM model. Provide the same one as given to the GroupChatManager.

    The config may contain the following:
    - code_execution_config: dict. The config for code execution. If not provided, code execution will be disabled.
    - human_input_mode: str. The mode for human input. One of "NEVER", "ALWAYS", "ASK".
    - description: str. A description of the agent for the agent and chat participants.
    - system_message: str. Initial system prompt for the agent.
    - functions: list. A list of functions to register. Each function should be a dict with the following keys:
        - name: str. The name of the function.
        - description: str. A description of the function for the agent.
        - function: function. The actual function to register.

    """

    def __init__(self, config=None):
        self.config = config or {}
        self.agent = self.build_agent()

    @property
    def name(self) -> str:
        "Agent name. Required. Must be provided in the config or defined in the subclass."
        return self.config["name"]

    @property
    def llm_config(self) -> dict:
        "LLM config. If none is provided, the default config will be used."
        return self.config.get("llm_config", DEFAULT_AGENT_CONFIG)

    @property
    def code_execution_config(self) -> Union[dict, False]:
        "Code execution config. If False is provided, code execution will be disabled."
        return self.config.get("code_execution_config", False)

    @property
    def human_input_mode(self) -> str:
        "Human input mode. Default is 'NEVER'."
        return self.config.get("human_input_mode", "NEVER")

    @property
    def description(self) -> str:
        "Agent description. Required. Must be provided in the config or defined in the subclass."
        return self.config["description"]

    @property
    def system_message(self) -> str:
        """
        Initial system message for the agent. Default is the default system
        message. Not required but recommended.
        """
        return self.config.get("system_message", AssistantAgent.DEFAULT_SYSTEM_MESSAGE)

    @property
    def max_consecutive_auto_reply(self) -> Union[int, None]:
        """
        Maximum number of consecutive auto replies. Default is None, which
        allows unlimited auto replies.
        """
        return self.config.get("max_consecutive_auto_reply", None)

    @property
    def functions(self) -> List[dict]:
        """
        List of functions to register with the agent. Optional. Functions must have the following keys, all required:
        - name: str. The name of the function.
        - description: str. A description of the function for the agent. Used by the agent to determine when to use the function.
        - callable_function: function. The actual function to register.
        """
        return self.config.get("functions", [])

    def build_agent(self) -> AssistantAgent:
        """
        Builds the agent with defined properties. If the properties are not defined in the subclass, the config values provided at initialization will be used.

        If functions are defined or were provided at initialization and user proxy was provided at config, the functions will be registered with the agent and user proxy.
        """

        if self.code_execution_config:
            agent = AssistantAgent(
                name=self.name,
                llm_config=self.llm_config,
                code_execution_config=self.code_execution_config,
                human_input_mode=self.human_input_mode,
                description=self.description,
                system_message=self.system_message,
                max_consecutive_auto_reply=self.max_consecutive_auto_reply,
            )
        else:
            agent = AssistantAgent(
                name=self.name,
                llm_config=self.llm_config,
                human_input_mode=self.human_input_mode,
                description=self.description,
                system_message=self.system_message,
                max_consecutive_auto_reply=self.max_consecutive_auto_reply,
            )

        if self.functions and self.config["user_proxy"]:
            agent, self.user_proxy = self.register_functions(
                agent, self.config["user_proxy"]
            )

        return agent

    def register_functions(
        self, agent, user_proxy
    ) -> Tuple[AssistantAgent, UserProxyAgent]:
        """
        Registers the functions in the config with the agent's llm config and user proxy. Returns the updated agent and updated user proxy.
        """
        agent_with_functions = agent
        user_proxy_with_functions = user_proxy

        functions = self.functions

        for f in functions:
            register_function(
                f["callable_function"],
                caller=agent_with_functions,
                executor=user_proxy_with_functions,
                description=f["description"],
            )

        return (agent_with_functions, user_proxy_with_functions)
