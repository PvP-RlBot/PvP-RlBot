import time

from util.io.game_state import GameState
from util.network.client import Client
from util.network.server import Server
from util.state_machine.state_machine import State

RECEPTION_TIMEOUT = 200


def get_timems():
    return round(time.time() * 1000)


class SynchronizationData:
    received_sync_data = None
    has_received_sync_data = False

    @staticmethod
    def receiveSyncData(data_str: str):
        SynchronizationData.received_sync_data = GameState.fromJSON(data_str)
        SynchronizationData.has_received_sync_data = True
        return None


class InitGameSyncWithOtherPlayer(State):
    def exec(self, param):
        return None

    def next(self, param):
        if Client.get_sid() >= Server.get_sids()[0]:
            return SendSyncData()
        return ReceiveSyncData()


class SendSyncData(State):
    def exec(self, param: GameState):
        Client.send_data(GameState.toJSON(param))
        return None

    def next(self, param):
        return ReceiveSyncData()


class ReceiveSyncData(State):
    def __init__(self):
        self.time_start = get_timems()

    def exec(self, param: GameState):
        # handled in the server thread
        return None

    def next(self, param):
        if SynchronizationData.has_received_sync_data:
            SynchronizationData.has_received_sync_data = False
            return SendSyncData()
        if (get_timems() - self.time_start) > RECEPTION_TIMEOUT:
            return SendSyncData()
        return self
