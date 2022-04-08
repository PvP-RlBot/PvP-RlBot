from util.network.client import Client
from util.network.connection.synchronization.alternator_states import get_starting_state, CommunicationData
from util.network.server import Server
from util.state_machine.state_machine import StateMachine


class SenderReceiverAlternator(StateMachine):
    def __init__(self, client: Client, server: Server, communication_data: CommunicationData):
        super().__init__(get_starting_state(client, server, communication_data))
