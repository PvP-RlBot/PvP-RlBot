from util.io.game_state import GameState
from util.state_machine.state_machine import State


class InitGameLogic(State):
    def exec(self, param: GameState):
        return None

    def next(self, param) -> State:
        return self
