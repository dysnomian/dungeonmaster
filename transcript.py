import os
import datetime

from sqlalchemy.sql import select
from models.game import Game
from db import session

from typing import Annotated, List

TRANSCRIPT_DIR = "tmp/transcripts/"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


class Transcript:
    def __init__(self, game_id: int):
        stmt = select(Game).where(Game.id == game_id)
        game = session.execute(stmt).scalars().first()
        if not game:
            print(f"Error: game with id {game_id} not found")
            return
        else:
            self.game = game

        self.transcript_filename = (
            f"{str(TRANSCRIPT_DIR)}game_{self.game.id}.transcript.md"
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
                    f"---\ndate_created: {self.timestamp()}\ngame_id: {self.game.id}\n---\n\n"
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
