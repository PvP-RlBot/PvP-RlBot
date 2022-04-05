import math

from util.math.orientation.orientation3 import Orientation3
from util.math.vector.vector3 import Vector3


class EulerZyxConverter:
    @staticmethod
    def toOrientation3(rotation):
        yaw = float(rotation.yaw)
        roll = float(rotation.roll)
        pitch = float(rotation.pitch)

        cr = math.cos(roll)
        sr = math.sin(roll)
        cp = math.cos(pitch)
        sp = math.sin(pitch)
        cy = math.cos(yaw)
        sy = math.sin(yaw)

        forward = Vector3(cp * cy, cp * sy, sp)
        up = Vector3(-cr*cy*sp-sr*sy, -cr*sy*sp+sr*cy, cp*cr)

        return Orientation3(forward, up)
