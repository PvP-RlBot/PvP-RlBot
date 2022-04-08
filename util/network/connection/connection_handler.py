from util.network.connection.connection_handler_states import InitConnection
from util.state_machine.state_machine import StateMachine


class GameSynchronizer(StateMachine):
    def __init__(self):
        super().__init__(InitConnection())
