import autogen
import matplotlib.pyplot as plt  # noqa E402
import networkx as nx  # noqa E402

from autogen.graph_utils import visualize_speaker_transitions_dict

from agents.character_sheet_team.character_sheet_leader import character_sheet_leader
from agents.character_sheet_team.player_character_expert import player_character_expert
from agents.character_sheet_team.character_sheet_json_composer import cs_json_composer
from agents.character_sheet_team.character_sheet_json_validator import cs_json_validator


team_members = [
    character_sheet_leader,
    player_character_expert,
    cs_json_composer,
    cs_json_validator
    ]

character_sheet_team_speaker_transitions = {
    character_sheet_leader: [
        player_character_expert,
        cs_json_composer,
        cs_json_validator
    ],
    player_character_expert: [
        character_sheet_leader,
        cs_json_composer,
        cs_json_validator
    ],
    cs_json_composer: [
        character_sheet_leader,
        player_character_expert,
        cs_json_validator
    ],
    cs_json_validator: [
        character_sheet_leader,
        cs_json_composer
    ],
}

visualize_speaker_transitions_dict(character_sheet_team_speaker_transitions, team_members)
plt.savefig("character_sheet_team.png")
