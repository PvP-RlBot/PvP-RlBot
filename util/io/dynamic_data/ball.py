from rlbot.utils.game_state_util import Physics

from util.math.vector.vector3 import Vector3


class BallData:
    def __init__(self, ball_physics: Physics):
        self.angular_velocity = Vector3(ball_physics.angular_velocity)
        self.position = Vector3(ball_physics.location)
        self.velocity = Vector3(ball_physics.velocity)
