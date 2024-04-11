import os
import json
import hashlib

from typing import Any, Dict, List, Annotated, NamedTuple

import jsonschema
from game_history import GameHistory

GAME_STATE_DIR = "json_data/games/"


def update_nested_structure(obj, path, new_value):
    """
    Recursively updates a nested value in the given JSON-like object.

    Args:
        obj (dict): The JSON-like object to update.
        path (list): A list of keys/indices representing the path to the value to update.
        new_value: The new value to set.
    """
    key = path[0]
    if isinstance(obj, dict):
        obj[key] = update_nested_structure(obj[key], path[1:], new_value)
    elif isinstance(obj, list):
        obj[int(key)] = update_nested_structure(obj[int(key)], path[1:], new_value)
    else:
        raise ValueError(f"Invalid path: {path}")

    return obj


class SaveResult(NamedTuple):
    success: bool
    checksum: str
    message: str
    filename: str


def get_game_state_files() -> List[Dict[str, Any]]:
    game_state_files = []
    for filename in os.listdir(GAME_STATE_DIR):
        if filename.endswith(".game_state.json"):
            game_state_files.append(get_game_summary(filename))
    return game_state_files


def get_game_summary(filename: Annotated[str, "filename"]) -> Dict[str, Any]:
    with open(GAME_STATE_DIR + filename, "r", encoding="utf-8") as f:
        game_state = json.load(f)
    summary = {
        "filename": filename,
        "last_modified": os.path.getmtime(GAME_STATE_DIR + filename),
        "game_name": game_state["game_name"],
        "meta": game_state["meta"],
    }
    return summary


def checksum(data: Annotated[Dict[str, Any], "data"]) -> str:
    return hashlib.md5(json.dumps(data).encode()).hexdigest()


class GameStateManager:
    def __init__(self, filename: Annotated[str, "filename"]):
        self.filename = filename
        self.state = self.fetch_state(filename)
        self.history = GameHistory(filename)
        self.schema = self.load_schema("json_data/schemas/game_state.schema.json")

    def checksum(self):
        return checksum(self.state)

    def fetch_state(self, filename: Annotated[str, "filename"]) -> Dict[str, Any]:
        with open(GAME_STATE_DIR + filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def refresh(self) -> bool:
        prev_checksum = self.checksum()
        self.state = self.fetch_state(self.filename)
        if prev_checksum != self.checksum():
            return True
        return False

    def load_schema(self, schema_file: Annotated[str, "schema_file"]) -> Dict[str, Any]:
        with open(schema_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def read_state(self) -> Annotated[Dict[str, Any], "data"]:
        self.fetch_state(self.filename)
        return self.state

    def validate(self, data: Annotated[Dict[str, Any], "data"]) -> List[str]:
        """
        Validate a game state against the schema and return a list of errors
        """
        if self.schema is None:
            raise ValueError("No schema loaded")
        else:
            try:
                jsonschema.validate(data, self.schema)
                return []
            except jsonschema.ValidationError as e:
                return [e.message]

    def update_value(
        self, path: List[str], new_value: Any
    ) -> Annotated[SaveResult, "save_result"]:
        """
        Update a value in the game state, using a path to traverse nested structures,
        validate the updated state, and save it to a file. If the updated state is not
        valid, return False and the validation errors, and do not save the state.

        Args:
            path (list): A list of keys/indices representing the path to the value to update.
            new_value: The new value to set.

        Returns:
        """
        # copy the current state
        updated_state = self.state.copy()

        # modify the state with the new value
        updated_state = update_nested_structure(updated_state, path, new_value)

        # validate the updated state
        errors = self.validate(updated_state)

        # if there are errors, return them
        if errors:
            return SaveResult(
                success=False,
                checksum=self.checksum(),
                message="Updated state is not valid. Errors: " + "\n".join(errors),
                filename=self.filename,
            )

        # update the state
        self.state = updated_state
        return self.save()

    def save(self) -> Annotated[SaveResult, "save_result"]:
        # update checksum from the current state
        current_checksum = checksum(self.state)

        # checksum the previous persisted state
        prev_state = self.fetch_state(self.filename)
        prev_state_checksum = checksum(prev_state)

        # is it actually different?
        if prev_state_checksum == current_checksum:
            return SaveResult(
                success=False,
                checksum=current_checksum,
                message=f"{self.filename} has not been modified",
                filename=self.filename,
            )

        # is it valid?
        errors = self.validate(self.state)
        if errors:
            message = "Updated state is not valid. Errors:"
            for error in errors:
                message += f"\n  {error}"
            return SaveResult(
                success=False,
                checksum=current_checksum,
                message=message,
                filename=self.filename,
            )

        # save the new state
        with open(GAME_STATE_DIR + self.filename, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

        # update the history
        self.history.append(current_checksum)

        return SaveResult(
            success=True,
            checksum=current_checksum,
            message=f"{self.filename} has been updated",
            filename=self.filename,
        )

    def name(self) -> str:
        return self.state["game_name"]

    def meta(self) -> Dict[str, Any]:
        return self.state["meta"]

    def sessions(self) -> Dict[str, Any]:
        return self.state["sessions"]

    def current_session(self) -> Dict[str, Any]:
        return self.state["sessions"]["current"]

    def campaign(self) -> Dict[str, Any]:
        return self.state["campaign"]

    def story(self) -> Dict[str, Any]:
        return self.campaign()["story"]

    def player_characters(self) -> List[Dict[str, Any]]:
        return self.campaign()["player_characters"]

    def character_sheet(self) -> Dict[str, Any]:
        return self.player_characters()[0]

    def npcs(self) -> Dict[str, Any]:
        return self.campaign()["npcs"]

    def locations(self) -> Dict[str, Any]:
        return self.campaign()["locations"]


class CombatManager:
    def __init__(self, state_manager: GameStateManager):
        self.state_manager = state_manager

    def in_combat(self) -> bool:
        return self.state_manager.read_state()["combat"]["currently_in_combat"]

    def combatants(self) -> List[str]:
        return self.state_manager.read_state()["combat"]["combatants"]

    def enter_combat(self) -> Annotated[SaveResult, "save_result"]:
        return self.state_manager.update_value(["combat", "currently_in_combat"], True)

    def exit_combat(self) -> Annotated[SaveResult, "save_result"]:
        return self.state_manager.update_value(["combat", "currently_in_combat"], False)
