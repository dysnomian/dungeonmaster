import os
import datetime

from game_state_manager import GameStateManager

from typing import Annotated, List

TRANSCRIPT_DIR = "tmp/transcripts/"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class Transcript:
    def __init__(self, state: GameStateManager):
        self.game_state = state
        self.transcript_filename = (
            TRANSCRIPT_DIR + self.game_state.name() + ".transcript.md"
        )
        self.create_transcript_file()

    def create_transcript_file(self) -> bool:
        if not os.path.exists(TRANSCRIPT_DIR):
            os.makedirs(TRANSCRIPT_DIR)

        if os.path.exists(self.transcript_filename):
            return False

        try:
            with open(self.transcript_filename, "w", encoding="utf-8") as f:
                f.write(
                    "---\ndate_created: "
                    + self.game_state.state["date_created"]
                    + "\ngame_id: "
                    + self.game_state.state["game_id"]
                    + "\n---\n\n"
                )
                f.write("# Game Transcript\n\n")
                return True
        except PermissionError:
            print(f"Error: permission denied to write to {self.transcript_filename}")
            return False

    def append(self, text: Annotated[str, "text"]) -> bool:
        try:
            with open(self.transcript_filename, "a", encoding="utf-8") as f:
                f.write(text)
                return True
        except PermissionError:
            print(f"Error: permission denied to write to {self.transcript_filename}")
            return False
        except FileNotFoundError:
            print(f"Error: transcript file {self.transcript_filename} not found")
            return False

    def append_message(self, message: str, sender: str) -> bool:
        self.append(self.format_message(message, sender))
        return True

    def format_message(self, message: str, sender: str) -> str:
        timestamp = self.timestamp()
        return f"{timestamp} {sender}: {message}\n\n----------\n\n"

    def timestamp(self) -> str:
        timestamp = datetime.datetime.now().strftime(TIMESTAMP_FORMAT)
        return timestamp

    def read_transcript(self) -> List[str]:
        """Read the contents of the transcript file, splitting on the message separator"""
        try:
            with open(self.transcript_filename, "r", encoding="utf-8") as f:
                return f.read().split("\n\n----------\n\n")
        except FileNotFoundError:
            print(f"Error: transcript file {self.transcript_filename} not found")
            return []
