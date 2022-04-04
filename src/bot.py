from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.io.bot_output import BotOutput


class Bot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)

    def initialize_agent(self):
        pass

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        b = BotOutput()
        b.throttle = 0
        return b
