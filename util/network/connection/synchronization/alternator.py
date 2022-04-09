from abc import abstractmethod

from util.coding_rules.override import Override
from util.io.game_state import GameState
from util.network.client import Client
from util.network.connection.synchronization.alternator_states import get_starting_state, CommunicationData
from util.network.server import Server
from util.state_machine.state_machine import StateMachine


class CommunicationStrategy:
    @abstractmethod
    def communicate(self, param: GameState):
        pass


class AlternatingCommunicationStrategy(CommunicationStrategy):
    def __init__(self, client: Client, server: Server, communication_data: CommunicationData):
        self.communication_state_machine = StateMachine(get_starting_state(client, server, communication_data))

    @Override(CommunicationStrategy)
    def communicate(self, param: GameState):
        self.communication_state_machine.exec(param)
