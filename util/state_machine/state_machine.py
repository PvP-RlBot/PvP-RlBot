from abc import ABC, abstractmethod

from util.io.game_state import GameState


class State(ABC):
    def start(self, param):
        pass

    def stop(self, param):
        pass

    @abstractmethod
    def exec(self, param):
        pass

    @abstractmethod
    def next(self, param):
        pass


class StateMachine(State):
    def __init__(self, init_state):
        self.state = None
        self.nextState = init_state

    def exec(self, param: GameState):
        if self.nextState is not self.state:
            self.nextState.start(param)
        self.state = self.nextState
        output = self.state.exec(param)
        self.nextState = self.state.next(param)
        if self.nextState is not self.state:
            self.state.stop(param)

        return output

    def next(self, param):
        return self
