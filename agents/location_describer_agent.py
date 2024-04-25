from typing import List, Union, Tuple, TYPE_CHECKING

from agents.agent_superclass import AgentSuperclass
from agents.functions.queries import get_current_location, get_game_tone

class LocationDescriberAgent(AgentSuperclass):

    @property
    def name(self) -> str:
        return "LocationDescriber"
    
    @property
    def description(self) -> str:
        return "Given the current location, adjacent locations, surrounding locations, recent transcript, other npcs in the location, story tone, and the current time, describes the location to the player."
    
    @property
    def system_message(self) -> str:
        return """
        You are the location describer. Given the current location, adjacent locations, surrounding locations, recent transcript, other npcs in the location, and the current time, describe the location to the player. Make the descriptions vivid but succinct and make them consistent with the intended story tone.

        If you add a new location, make sure to describe it in a way that is consistent with the story tone and the player's expectations. If the location is a key location, make sure to include any relevant information about the location that the player should know.

        If you add important details to a location, add them to the Location record in the database.
        """
    
    @property
    def code_execution_config(self) -> dict:
        return {"last_n_messages": 10, "work_dir": "json_data/games/"}
    
    @property
    def functions(self) -> List[dict]:
        return [
            {
                "name": "get_current_location",
                "description": "Read the current location from the database.",
                "callable_function": get_current_location,
            },
            {
                "name": "get_game_tone",
                "description": "Read the intended game tone from the database.",
                "callable_function": get_game_tone,
            }
        ]