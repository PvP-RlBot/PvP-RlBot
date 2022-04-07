from util.network.connection.synchronization.alternator_states import get_starting_state
from util.state_machine.state_machine import StateMachine


class SenderReceiverAlternator(StateMachine):
    def __init__(self):
        super().__init__(get_starting_state())
