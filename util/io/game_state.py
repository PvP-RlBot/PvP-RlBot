from typing import List

from util.io.dynamic_data.ball import BallData
from util.io.dynamic_data.car import CarData
from util.io.misc_info.team import Team

from rlbot.utils.structures.game_data_struct import GameTickPacket


class GameState:
    def __init__(self, packet: GameTickPacket, previous_game_state, index: int):
        self.index = index
        self.car_list = []
        for car in packet.game_cars:
            team = Team.idToTeam(car.team)
            self.car_list.append(CarData(car, team))
        self.previous_game_state = previous_game_state
        if self.previous_game_state is not None:
            self.previous_game_state.previous_game_state = None
        self.human_car_list = self.__generateHumanCarList(self.car_list)
        self.car = self.car_list[index]
        self.team = self.car.team
        self.ball = BallData(packet.game_ball.physics)

    @staticmethod
    def __generateHumanCarList(car_list: List[CarData]):
        human_car_list = []
        for car in car_list:
            if not car.is_bot:
                human_car_list.append(car)
        return human_car_list
