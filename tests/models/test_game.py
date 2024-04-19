import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import engine
from models import Game
from models.base import Base


class TestGame:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_game_model(self):
        # Create a new game instance
        new_game = Game(
            name="Test Game",
            rules_set="Test Rules",
            game_length="1 hour",
            session_length="30 minutes",
            tone="Serious",
            difficulty="Hard",
            setting="Fantasy",
            npc_death_allowed=True,
        )
        print(new_game)

        # Add new game to the session
        self.session.add(new_game)
        self.session.commit()

        # Query the game from the database
        statement = select(Game).where(Game.name == "Test Game")
        game_in_db = self.session.scalars(statement).one()

        # Check if the game was added correctly
        assert game_in_db.name == "Test Game"
        assert game_in_db.rules_set == "Test Rules"
        assert game_in_db.game_length == "1 hour"
        assert game_in_db.session_length == "30 minutes"
        assert game_in_db.tone == "Serious"
        assert game_in_db.difficulty == "Hard"
        assert game_in_db.setting == "Fantasy"
        assert game_in_db.npc_death_allowed is True
