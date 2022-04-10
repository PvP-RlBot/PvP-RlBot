from util.io.game_state import GameState
from util.logging.logging import Logger
from util.network.connection.connection_handler_states import TryConnectingWithConfigFile
from util.state_machine.state_machine import StateMachine


class GameSynchronizer:
    def __init__(self, logger: Logger):
        self.synchronizer_state_machine = StateMachine(TryConnectingWithConfigFile(logger))

    def synchronize(self, param: GameState):
        return self.synchronizer_state_machine.exec(param)
