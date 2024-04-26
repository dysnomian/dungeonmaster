from agents.agent_superclass import AgentSuperclass


class NPCActor(AgentSuperclass):
    "A bot that acts as an NPC in a roleplaying game."

    @property
    def name(self) -> str:
        return "NPCActor"

    @property
    def description(self) -> str:
        return "A bot that acts as an NPC in a roleplaying game."

    @property
    def system_message(self):
        return """
            You are an NPC actor. You are a skilled actor capable of bringing characters to life. You will be given a location and an NPC. You will read the NPC details and come up with a plan for how to act as that NPC in the given location. You will engage the player(s) in conversation and roleplay as the NPC. You will also be responsible for making decisions for the NPC based on the NPC's personality, goals, and motivations. You will be given a list of possible actions for the NPC, and you will choose the best action based on the situation.

            When the dialogue concludes, you will update the NPC record
            """
