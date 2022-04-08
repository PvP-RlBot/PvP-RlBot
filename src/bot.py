import time

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.network.connection.connection_handler import GameSynchronizer
from util.io.bot_output import BotOutput
from util.io.game_state import GameState


class Bot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.index = index
        self.game_synchronizer = GameSynchronizer()

    def initialize_agent(self):
        pass

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        game_state = GameState(packet, self.index)
        self.game_synchronizer.exec(game_state)
        self.set_game_state(game_state.toFrameworkGameState())
        return BotOutput()
