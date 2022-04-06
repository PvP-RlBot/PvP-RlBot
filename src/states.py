from threading import Thread

from src.physics.game_sync import InitGameSyncWithOtherPlayer
from util.io.game_state import GameState
from util.network.client import Client
from util.network.server import Server
from util.state_machine.state_machine import State, StateMachine


def connected():
    return Client.is_connected() and Server.amount_of_connections() > 0


class InitBotState(State):
    def exec(self, param: GameState):
        return None

    def next(self, param) -> State:
        return ConnectToOtherPlayer()


class ConnectToOtherPlayer(State):
    def start(self, param):
        Thread(target=Server.start).start()
        Thread(target=Client.start).start()

    def exec(self, param):
        return None

    def next(self, param):
        if connected():
            return ConnectionEstablished()
        return self


class ConnectionEstablished(State):
    def __init__(self):
        self.machine = StateMachine(InitGameSyncWithOtherPlayer())

    def start(self, param):
        print('Connected')

    def stop(self, param):
        print('Disconnected from other player!')

    def exec(self, param):
        return self.machine.exec(param)

    def next(self, param):
        if not connected():
            return TryReconnection()
        return self


class TryReconnection(State):
    def start(self, param):
        print('Trying to reconnect...')

    def exec(self, param):
        return None

    def next(self, param):
        if connected():
            return ConnectionEstablished()
        return self
