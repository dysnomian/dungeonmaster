"""
The DiceRoller agent class and its included functions. It rolls dice using the CritDice
syntax and reports the result.
"""

from typing import Annotated, Tuple, List

import rolldice

from agent_superclass import AgentSuperclass


def roll(
    dice_expression: Annotated[
        str, "Dice expression to be evaluated in the CritDice syntax"
    ],
) -> Tuple[int, str]:
    "Roll dice using the CritDice syntax"
    return rolldice.roll_dice(dice_expression)


class DiceRoller(AgentSuperclass):
    "A bot that rolls dice using the CritDice syntax."

    @property
    def name(self) -> str:
        return "DiceRoller"

    @property
    def description(self) -> str:
        return "A bot that rolls dice using the CritDice syntax."

    @property
    def system_message(self):
        return (
            """
            You are a dice rolling bot. You watch for dice rolls in the conversation and respond with the result. You can roll any number of dice with any number of sides. You can also add or subtract numbers from the result. You use the CritDice syntax and the `roll` function to roll dice.

            """
            + self.__critdice_syntax()
        )

    @property
    def functions(self) -> List[dict]:
        return [
            {
                "name": "roll",
                "description": "Roll dice using the CritDice syntax",
                "callable_function": roll,
            }
        ]

    def __critdice_syntax(self) -> str:
        with open("critdice_syntax.md", "r", encoding="utf-8") as f:
            return f.read()
