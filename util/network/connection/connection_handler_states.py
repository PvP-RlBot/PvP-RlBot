from threading import Thread

import jsonpickle

from util.io.game_state import GameState
from util.network.client import Client
from util.network.connection.connection_gui import ConnectionGUI
from util.network.connection.synchronization.alternator import SenderReceiverAlternator
from util.network.connection.synchronization.alternator_states import CommunicationData
from util.network.connection.communication_data import CommunicationDataBuilder
from util.network.server import Server
from util.state_machine.state_machine import State


def connected(client: Client, server: Server):
    return client.is_connected() and server.amount_of_connections() > 0


class InitConnection(State):
    def exec(self, param):
        pass

    def next(self, param):
        return TryConnectingWithConfigFile()


def is_config_file_invalid(communication_data_from_cfg):
    return communication_data_from_cfg is None


class TryConnectingWithConfigFile(State):
    def __init__(self):
        f = open("src/network_connection.cfg", "r")
        self.communication_data_from_cfg = CommunicationData.asCommunicationData(jsonpickle.decode(f.read()))
        f.close()

    def exec(self, param):
        pass

    def next(self, param):
        if is_config_file_invalid(self.communication_data_from_cfg):
            return AskNetworkInfoGUI()
        return ConnectToOtherPlayer(self.communication_data_from_cfg)


class AskNetworkInfoGUI(State):
    def __init__(self):
        self.connection_gui = ConnectionGUI()

    def exec(self, param):
        self.connection_gui.update()

    def stop(self, param):
        self.connection_gui.quit()

    def next(self, param):
        if self.connection_gui.has_requested_connection:
            communication_data = CommunicationDataBuilder()\
                .withURL(self.connection_gui.client_url)\
                .withHost(self.connection_gui.server_host)\
                .withPort(self.connection_gui.server_port)\
                .build()
            f = open("src/network_connection.cfg", "w")
            f.write(jsonpickle.encode(communication_data, indent=4))
            f.close()
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

    def start(self, param):
        self.server.set_reception_callback(self.communication_data.receiveSyncData)
        server_args = (self.communication_data.server_host, self.communication_data.server_port)
        client_args = (self.communication_data.client_url,)
        self.server_connection_thread = Thread(target=self.server.start, args=server_args)
        self.client_connection_thread = Thread(target=self.client.start, args=client_args)
        self.server_connection_thread.start()
        self.client_connection_thread.start()

    def exec(self, param):
        pass

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
        self.send_receive_alternator = SenderReceiverAlternator(client, server, communication_data)

    def start(self, param):
        print('Connected to other player!')
        print('client url: ', self.communication_data.client_url)
        print('server host:', self.communication_data.server_host)
        print('server port:', self.communication_data.server_port)

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
