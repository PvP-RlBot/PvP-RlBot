from rlbot.messages.flat.PlayerInfo import PlayerInfo

from util.io.misc_info.team import Team
from util.math.orientation.euler_zyx_converter import EulerZyxConverter
from util.math.vector.vector3 import Vector3


class CarData:
    def __init__(self, player_info: PlayerInfo, team: Team):
        self.player_info = player_info
        self.isBot = player_info.IsBot()
        self.position = Vector3(player_info.Physics().Location())
        self.velocity = Vector3(player_info.Physics().Velocity())
        self.orientation = EulerZyxConverter.toOrientation3(player_info.Physics().Rotation())
        self.team = team
