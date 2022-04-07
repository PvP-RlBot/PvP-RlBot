from util.network.connection.connection_handler_states import InitConnection
from util.network.connection.synchronization.alternator_states import SynchronizationData
from util.network.server import Server
from util.state_machine.state_machine import StateMachine


class GameSynchronizer(StateMachine):
    def __init__(self):
        super().__init__(InitConnection())
        Server.set_reception_callback(SynchronizationData.receiveSyncData)
