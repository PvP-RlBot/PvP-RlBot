from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from src.states import InitBotState
from util.io.bot_output import BotOutput
from util.io.game_state import GameState
from util.state_machine.state_machine import StateMachine


class Bot(BaseAgent):
    def __init__(self, name, team, index):
        super().__init__(name, team, index)
        self.index = index
        self.main_state_machine = StateMachine(InitBotState())
        self.previous_game_state = None

    def initialize_agent(self):
        pass

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        game_state = GameState(packet, self.previous_game_state, self.index)
        self.main_state_machine.exec(None)
        self.previous_game_state = game_state
        return BotOutput()
