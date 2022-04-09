from threading import Thread

import jsonpickle

from util.coding_rules.override import Override
from util.io.game_state import GameState
from util.network.client import Client
from util.network.connection.connection_gui import ConnectionGUI
from util.network.connection.synchronization.alternator import AlternatingCommunicationStrategy
from util.network.connection.synchronization.alternator_states import CommunicationData
from util.network.connection.communication_data import CommunicationDataBuilder
from util.network.server import Server
from util.state_machine.state_machine import State


def connected(client: Client, server: Server):
    return client.is_connected() and server.amount_of_connections() > 0


class TryConnectingWithConfigFile(State):
    def __init__(self):
        file = open("src/network_connection.cfg", "r")
        self.communication_data_from_cfg = CommunicationData.validateCommunicationData(jsonpickle.decode(file.read()))
        file.close()

    @Override(State)
    def next(self, param):
        if CommunicationData.is_config_file_invalid(self.communication_data_from_cfg):
            return AskNetworkInfoGUI()
        return ConnectToOtherPlayer(self.communication_data_from_cfg)


class AskNetworkInfoGUI(State):
    def __init__(self):
        self.connection_gui = ConnectionGUI()

    @Override(State)
    def exec(self, param):
        self.connection_gui.update()

    @Override(State)
    def stop(self, param):
        self.connection_gui.quit()

    @Override(State)
    def next(self, param):
        if self.connection_gui.has_requested_connection:
            communication_data = CommunicationDataBuilder()\
                .withURL(self.connection_gui.client_url)\
                .withHost(self.connection_gui.server_host)\
                .withPort(self.connection_gui.server_port)\
                .build()
            file = open("src/network_connection.cfg", "w")
            file.write(jsonpickle.encode(communication_data, indent=4))
            file.close()
            return ConnectToOtherPlayer(communication_data)
        return self


def cannotConnectToOtherPlayer(thread1: Thread, thread2: Thread):
    return not (thread1.is_alive() and thread2.is_alive())


class ConnectToOtherPlayer(State):
    def __init__(self, communication_data: CommunicationData):
        self.client = Client()
        self.server = Server()
        self.communication_data = communication_data
        self.client_connection_thread = None
        self.server_connection_thread = None

    @Override(State)
    def start(self, param):
        self.server.set_reception_callback(self.communication_data.receiveSyncData)
        server_args = (self.communication_data.server_host, self.communication_data.server_port)
        client_args = (self.communication_data.client_url,)
        self.server_connection_thread = Thread(target=self.server.start, args=server_args)
        self.client_connection_thread = Thread(target=self.client.start, args=client_args)
        self.server_connection_thread.start()
        self.client_connection_thread.start()

    @Override(State)
    def next(self, param):
        if connected(self.client, self.server):
            return ConnectionEstablished(self.client, self.server, self.communication_data)
        if cannotConnectToOtherPlayer(self.server_connection_thread, self.client_connection_thread):
            self.server.stop()
            self.client.stop()
            return AskNetworkInfoGUI()
        return self


class ConnectionEstablished(State):
    def __init__(self, client: Client, server: Server, communication_data: CommunicationData):
        self.client = client
        self.server = server
        self.communication_data = communication_data
        self.communication_strategy = AlternatingCommunicationStrategy(client, server, communication_data)

    @Override(State)
    def start(self, param):
        print('Connected to other player!')
        print('client url: ', self.communication_data.client_url)
        print('server host:', self.communication_data.server_host)
        print('server port:', self.communication_data.server_port)

    @Override(State)
    def stop(self, param):
        print('Disconnected from other player!')

    @Override(State)
    def exec(self, param: GameState):
        return self.communication_strategy.communicate(param)

    @Override(State)
    def next(self, param):
        if not connected(self.client, self.server):
            return TryReconnection(self.client, self.server, self.communication_data)
        return self


class TryReconnection(State):
    def __init__(self, client: Client, server: Server, communication_data: CommunicationData):
        self.client = client
        self.server = server
        self.communication_data = communication_data

    @Override(State)
    def start(self, param):
        print('Trying to reconnect to other player...')

    # reconnection is done automatically in the client thread

    @Override(State)
    def next(self, param):
        if connected(self.client, self.server):
            return ConnectionEstablished(self.client, self.server, self.communication_data)
        return self
