from rlbot.utils.structures.game_data_struct import PlayerInfo

from util.io.misc_info.team import Team
from util.math.orientation.euler_zyx_converter import EulerZyxConverter
from util.math.vector.vector3 import Vector3


class CarData:
    def __init__(self, player_info: PlayerInfo):
        self.player_info = player_info
        self.is_bot = player_info.is_bot
        self.position = Vector3(player_info.physics.location)
        self.velocity = Vector3(player_info.physics.velocity)
        self.orientation = EulerZyxConverter.toOrientation3(player_info.physics.rotation)
        self.team = Team.idToTeam(player_info.team)
