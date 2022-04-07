from threading import Thread

from util.io.game_state import GameState
from util.network.client import Client
from util.network.connection.synchronization.alternator import SenderReceiverAlternator
from util.network.server import Server
from util.state_machine.state_machine import State


def connected():
    return Client.is_connected() and Server.amount_of_connections() > 0


class InitConnection(State):
    def exec(self, param):
        pass

    def next(self, param):
        return ConnectToOtherPlayer()


class ConnectToOtherPlayer(State):
    def start(self, param):
        Thread(target=Server.start).start()
        Thread(target=Client.start).start()

    def exec(self, param):
        pass

    def next(self, param):
        if connected():
            return ConnectionEstablished()
        return self


class ConnectionEstablished(State):
    def __init__(self):
        self.send_receive_alternator = SenderReceiverAlternator()

    def start(self, param):
        print('Connected')

    def stop(self, param):
        print('Disconnected from other player!')

    def exec(self, param: GameState):
        return self.send_receive_alternator.exec(param)

    def next(self, param):
        if not connected():
            return TryReconnection()
        return self


class TryReconnection(State):
    def start(self, param):
        print('Trying to reconnect...')

    def exec(self, param):
        pass

    def next(self, param):
        if connected():
            return ConnectionEstablished()
        return self
