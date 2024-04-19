import os

from typing import List, Annotated

GAME_STATE_DIR = "json_data/games/"


class GameHistory:
    def __init__(self, game_state_filename) -> None:
        self.game_state_filename = game_state_filename
        self.history_filename = game_state_filename + ".history"
        self.create_history_file()

    @classmethod
    def find_or_create(cls, game_id: str) -> "GameHistory":
        game_name = Game.find_by_id(game_id).name
        history_filename = game_name + ".history"

    def current(self) -> str:
        if self.fetch() == []:
            return None
        return self.fetch()[-1]

    def last(self) -> str:
        if len(self.fetch()) < 2:
            return None
        return self.fetch()[-2]

    def fetch(self) -> Annotated[List[str], "history"]:
        if self.create_history_file():
            return []

        with open(GAME_STATE_DIR + self.history_filename, "r", encoding="utf-8") as f:
            return f.read().splitlines()

    def create_history_file(self) -> bool:
        if not os.path.exists(GAME_STATE_DIR + self.history_filename):
            with open(
                GAME_STATE_DIR + self.history_filename, "w", encoding="utf-8"
            ) as f:
                f.write("")
            return True

        return False

    def append(self, checksum: Annotated[str, "checksum"]) -> List[str]:
        if self.fetch() != [] and checksum == self.current():
            print(f"Error: {checksum} already exists in {self.history_filename}")
            return self.fetch()

        print(f"Appending {checksum} to {self.history_filename}")
        with open(GAME_STATE_DIR + self.history_filename, "a", encoding="utf-8") as f:
            f.write(checksum + "\n")
        return self.fetch()
