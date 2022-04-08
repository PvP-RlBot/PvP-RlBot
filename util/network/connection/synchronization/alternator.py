from util.network.client import Client
from util.network.connection.synchronization.alternator_states import get_starting_state, SynchronizationData
from util.network.server import Server
from util.state_machine.state_machine import StateMachine


class SenderReceiverAlternator(StateMachine):
    def __init__(self, client: Client, server: Server, synchronization_data: SynchronizationData):
        super().__init__(get_starting_state(client, server, synchronization_data))
