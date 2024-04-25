import json

from typing import Annotated, List, Dict, TYPE_CHECKING

from agents.functions.queries import find_game, find_player, find_character_sheets, find_campaign, update_campaign_story


if TYPE_CHECKING:
    from models.player import Player
    from models.game import Game
    from models.character_sheet import CharacterSheet
    from models.background import Background
    from models.race import Race

from agents.agent_superclass import AgentSuperclass


STARTING_GAME_ID = 1


def get_game_context(
    game_id: Annotated[int, "The id of the game being played."],
    player_id: Annotated[int, "The id of the current player."],
    player_character_ids: Annotated[List[int], "The id of the character sheet the player is using."],
) -> str:
    game = find_game(game_id)
    player = find_player(player_id)
    pcs = find_character_sheets(player_character_ids)

    pcs_list = []
    for pc in pcs:
        class_levels = pc.class_levels
        class_names = list(set([cls["name"] for cls in class_levels]))
        pcs_list.append({
            "name": pc.name,
            "class_names": class_names,
            "background": pc.background.name,
            "race": pc.race.name,
            "alignment": pc.alignment,
            "backstory": pc.backstory
        })

    game_context = f"""
    Game:\n
    Game Length: {game.game_length__sessions} session(s)
    Session Length: {game.session_length__responses}
    response(s)\nTone: {game.tone}\n
    Setting: {game.setting}\n
    \n
    Player Veils (topics to do only off-screen): {player.veils}\n
    Player Lines (topics to never do): {player.lines}\n
    Player Loves (topics to include liberally): {player.loves}\n
    Player Likes (topics to include judiciously): {player.likes}\n
    \n
    Player Characters:\n
    {pcs_list}
    """

    return game_context

def update_story(
    game_id: Annotated[int, "The id of the game being played."],
    summary: Annotated[str, "1-2 sentence summary of the plot"],
    primary_goal: Annotated[str, "The primary goal of the game. When the player achieves this goal, the game will conclude."],
    secondary_goals: Annotated[List[str], "The secondary goals of the game. Achieving these goals will help the player achieve the primary goal but are not strictly necessary. These can be adjusted, added to, or removed as the game progresses."],
    steps: Annotated[Dict[str, List[str]], "The steps the player can take to achieve each goal. These can be adjusted, added to, or removed as the game progresses. Each step should be a clear, actionable task that the player can complete. Each goal should have 2 to 4 steps."],
    obstacles: Annotated[List[str], "The obstacles the players will face. while trying to achieve the goals."],
    setting_notes: Annotated[str, "Any notes on the setting that will be relevant to describing scenes or characterizing NPCs."],
    key_friendlies: Annotated[List[str], "The key friendly characters in the game with an eye to their funciton in the plot. This will be given to the NPC creator to flesh out"],
    key_antagonists: Annotated[List[str], "The key antagonists in the game with an eye to their function in the plot. This will be given to the NPC creator to flesh out"]
) -> None:
    story = json.dumps({
        "summary": summary,
        "primary_goal": primary_goal,
        "secondary_goals": secondary_goals,
        "steps": steps,
        "obstacles": obstacles,
        "setting_notes": setting_notes,
        "key_friendlies": key_friendlies,
        "key_antagonists": key_antagonists
    })

    update_campaign_story(game_id, story)

def get_campaign_story(game_id: Annotated[int, "The id of the game being played."]) -> Dict[str, str]:
    campaign = find_campaign(game_id)
    return campaign.story


class PlotWriterAgent(AgentSuperclass):

    @property
    def name(self) -> str:
        return "PlotWriter"

    @property
    def description(self) -> str:
        return "Given game context, player context, and game config, generates an outline of the plot and updates it as the game progresses."

    @property
    def system_message(self) -> str:
        return """
        You are the plot writer. You are responsible for generating the plot of the game and updating it as the game progresses.

        Given the game length, session length, difficulty, tone, players' veils and lines (if any), and the player's character sheets, you will generate an outline of the plot.

        When generating a plot, you come up with a series of events that will happen in the game. These events should be interesting, challenging, and engaging for the players. They should also be tailored to the players' character backstory and the game's setting, if provided.

        Come up with an engaging and intriguing premise for the game. This could be a mystery, a heist, a political intrigue, or anything else that you think would be fun for the players. Write a brief "elevator pitch" summary that intrigues the players and sets the tone for the game and conceals the plot twists and surprises.

        Given a number of sessions, come up with a goal for each session. This could be a major plot point, a character development moment, or a challenge for the players to overcome. Make sure that each session has a clear goal and moves the plot forward. Come up with a series of steps the players could take to achieve that goal, and a series of obstacles they might face along the way.
        """

    @property
    def code_execution_config(self) -> dict:
        return {"last_n_messages": 10, "work_dir": "json_data/games/"}

    @property
    def functions(self) -> List[dict]:
        return [
            {
                "name": "get_game_context",
                "description": "Read the game context from the database.",
                "callable_function": get_game_context,
            },
            {
                "name": "update_story",
                "description": "Update the story in the database.",
                "callable_function": update_story,
            },
            {
                "name": "get_campaign_story",
                "description": "Read the campaign story from the database.",
                "callable_function": get_campaign_story,
            },
        ]
