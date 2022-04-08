import time

from util.io.game_state import GameState
from util.network.client import Client
from util.network.server import Server
from util.state_machine.state_machine import State

RECEPTION_TIMEOUT = 200


def get_timems():
    return round(time.time() * 1000)


def should_start_by_sending_data(client: Client, server: Server):
    return client.get_sid() >= server.get_sids()[0]


class SynchronizationData:
    def __init__(self):
        self.received_sync_data = None

    def receiveSyncData(self, data: str):
        self.received_sync_data = GameState.fromJSON(data)


class SendSyncData(State):
    def __init__(self, client: Client, synchronization_data: SynchronizationData):
        self.client = client
        self.synchronization_data = synchronization_data

    def exec(self, param: GameState):
        self.client.send_data(GameState.toJSON(param))

    def next(self, param):
        return ReceiveSyncData(self.client, self.synchronization_data)


class ReceiveSyncData(State):
    def __init__(self, client: Client, synchronization_data: SynchronizationData):
        self.time_start = get_timems()
        self.client = client
        self.synchronization_data = synchronization_data

    def exec(self, param: GameState):
        # handled in the server thread
        pass

    def stop(self, param: GameState):
        param.update_with_sync_data(self.synchronization_data.received_sync_data)
        self.synchronization_data.received_sync_data = None

    def next(self, param):
        if self.synchronization_data.received_sync_data is not None:
            return SendSyncData(self.client, self.synchronization_data)
        if (get_timems() - self.time_start) > RECEPTION_TIMEOUT:
            return SendSyncData(self.client, self.synchronization_data)
        return self


def get_starting_state(client: Client, server: Server, synchronization_data: SynchronizationData):
    if should_start_by_sending_data(client, server):
        return SendSyncData(client, synchronization_data)
    return ReceiveSyncData(client, synchronization_data)
