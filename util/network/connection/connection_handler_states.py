from threading import Thread

from util.io.game_state import GameState
from util.network.client import Client
from util.network.connection.synchronization.alternator import SenderReceiverAlternator
from util.network.connection.synchronization.alternator_states import SynchronizationData
from util.network.server import Server
from util.state_machine.state_machine import State


def connected(client: Client, server: Server):
    return client.is_connected() and server.amount_of_connections() > 0


class InitConnection(State):
    def exec(self, param):
        pass

    def next(self, param):
        return ConnectToOtherPlayer(SynchronizationData())


class ConnectToOtherPlayer(State):
    def __init__(self, synchronization_data: SynchronizationData):
        self.client = Client()
        self.server = Server()
        self.synchronization_data = synchronization_data

    def start(self, param):
        self.server.set_reception_callback(self.synchronization_data.receiveSyncData)
        Thread(target=self.server.start).start()
        Thread(target=self.client.start).start()

    def exec(self, param):
        pass

    def next(self, param):
        if connected(self.client, self.server):
            return ConnectionEstablished(self.client, self.server, self.synchronization_data)
        return self


class ConnectionEstablished(State):
    def __init__(self, client: Client, server: Server, synchronization_data: SynchronizationData):
        self.client = client
        self.server = server
        self.send_receive_alternator = SenderReceiverAlternator(client, server, synchronization_data)

    def start(self, param):
        print('Connected to other player!')

    def stop(self, param):
        print('Disconnected from other player!')

    def exec(self, param: GameState):
        return self.send_receive_alternator.exec(param)

    def next(self, param):
        if not connected(self.client, self.server):
            return TryReconnection(self.client, self.server)
        return self


class TryReconnection(State):
    def __init__(self, client: Client, server: Server):
        self.client = client
        self.server = server

    def start(self, param):
        print('Trying to reconnect to other player...')

    def exec(self, param):
        pass

    def next(self, param):
        if connected(self.client, self.server):
            return ConnectionEstablished(self.client, self.server)
        return self
