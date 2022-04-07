from typing import List

import jsonpickle

import rlbot.utils.game_state_util as framework_utils

from util.io.dynamic_data.ball import BallData
from util.io.dynamic_data.car import CarData

from rlbot.utils.structures.game_data_struct import GameTickPacket


class GameState:
    def __init__(self, packet: GameTickPacket, index: int):
        self.index = index
        self.car_list = []
        for car in packet.game_cars:
            self.car_list.append(CarData(car))
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

    def update_with_sync_data(self, received_sync_data):
        pass

    def toFrameworkGameState(self):
        ball_state = framework_utils.BallState(
            framework_utils.Physics(location=self.ball.position.to_game_state_vector3(),
                                    velocity=self.ball.velocity.to_game_state_vector3()))
        return framework_utils.GameState(ball=ball_state)

    @classmethod
    def toJSON(cls, game_state):
        return jsonpickle.encode(game_state)

    @classmethod
    def fromJSON(cls, received_sync_data):
        return jsonpickle.decode(received_sync_data)
