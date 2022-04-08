import time

from util.io.game_state import GameState
from util.network.client import Client
from util.network.connection.synchronization.communication_data import CommunicationData
from util.network.server import Server
from util.state_machine.state_machine import State

RECEPTION_TIMEOUT = 200


def get_timems():
    return round(time.time() * 1000)


def should_start_by_sending_data(client: Client, server: Server):
    return client.get_sid() >= server.get_sids()[0]


def is_data_received(synchronization_data: CommunicationData):
    return synchronization_data.received_sync_data is not None


def is_reception_timeout_reached(time_start: int):
    return (get_timems() - time_start) > RECEPTION_TIMEOUT


class SendSyncData(State):
    def __init__(self, client: Client, communication_data: CommunicationData):
        self.client = client
        self.communication_data = communication_data

    def exec(self, param: GameState):
        self.client.send_data(GameState.toJSON(param))

    def next(self, param):
        return ReceiveSyncData(self.client, self.communication_data)


class ReceiveSyncData(State):
    def __init__(self, client: Client, communication_data: CommunicationData):
        self.time_start = get_timems()
        self.client = client
        self.communication_data = communication_data

    def exec(self, param: GameState):
        # handled in the server thread
        pass

    def stop(self, param: GameState):
        param.update_with_sync_data(self.communication_data.received_sync_data)
        self.communication_data.received_sync_data = None

    def next(self, param):
        if is_data_received(self.communication_data):
            return SendSyncData(self.client, self.communication_data)
        if is_reception_timeout_reached(self.time_start):
            return SendSyncData(self.client, self.communication_data)
        return self


def get_starting_state(client: Client, server: Server, communication_data: CommunicationData):
    if should_start_by_sending_data(client, server):
        return SendSyncData(client, communication_data)
    return ReceiveSyncData(client, communication_data)
