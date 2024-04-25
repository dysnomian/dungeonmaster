"""
Given a player's response, the evaluator agent will determine what changes need to happen next and dispatch them to the appropriate agents.
"""

import logging
from typing import Annotated, List, Union

from agents.agent_superclass import AgentSuperclass

class EvaluatorAgent(AgentSuperclass):
    def __init__(self, config: dict):
        super().__init__(config)
        self.logger = logging.getLogger(__name__)

    def evaluate_response(self, response: str) -> None:
        self.logger.info(f"Evaluating response: {response}")