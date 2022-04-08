from threading import Thread

from util.io.game_state import GameState
from util.network.client import Client
from util.network.connection.connection_gui import ConnectionGui
from util.network.connection.synchronization.alternator import SenderReceiverAlternator
from util.network.connection.synchronization.alternator_states import CommunicationData
from util.network.connection.synchronization.communication_data import CommunicationDataBuilder
from util.network.server import Server
from util.state_machine.state_machine import State


def connected(client: Client, server: Server):
    return client.is_connected() and server.amount_of_connections() > 0


class InitConnection(State):
    def __init__(self):
        self.connection_gui = ConnectionGui()

    def exec(self, param):
        self.connection_gui.update()

    def stop(self, param):
        self.connection_gui.quit()

    def next(self, param):
        if self.connection_gui.has_requested_connection:
            communication_data = CommunicationDataBuilder()\
                .withURL(self.connection_gui.client_url)\
                .withHost(self.connection_gui.server_host)\
                .withPort(self.connection_gui.server_port)
            return ConnectToOtherPlayer(communication_data.build())
        return self


class ConnectToOtherPlayer(State):
    def __init__(self, communication_data: CommunicationData):
        self.client = Client()
        self.server = Server()
        self.communication_data = communication_data

    def start(self, param):
        self.server.set_reception_callback(self.communication_data.receiveSyncData)
        Thread(target=self.server.start, args=(self.communication_data.host, self.communication_data.port)).start()
        Thread(target=self.client.start, args=(self.communication_data.url,)).start()

    def exec(self, param):
        pass

    def next(self, param):
        if connected(self.client, self.server):
            return ConnectionEstablished(self.client, self.server, self.communication_data)
        return self


class ConnectionEstablished(State):
    def __init__(self, client: Client, server: Server, communication_data: CommunicationData):
        self.client = client
        self.server = server
        self.communication_data = communication_data
        self.send_receive_alternator = SenderReceiverAlternator(client, server, communication_data)

    def start(self, param):
        print('Connected to other player!')

    def stop(self, param):
        print('Disconnected from other player!')

    def exec(self, param: GameState):
        return self.send_receive_alternator.exec(param)

    def next(self, param):
        if not connected(self.client, self.server):
            return TryReconnection(self.client, self.server, self.communication_data)
        return self


class TryReconnection(State):
    def __init__(self, client: Client, server: Server, communication_data: CommunicationData):
        self.client = client
        self.server = server
        self.communication_data = communication_data

    def start(self, param):
        print('Trying to reconnect to other player...')

    def exec(self, param):
        pass

    def next(self, param):
        if connected(self.client, self.server):
            return ConnectionEstablished(self.client, self.server, self.communication_data)
        return self
