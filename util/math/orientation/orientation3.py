from util.math.vector.vector3 import Vector3


class Orientation3:
    """
    This class describes the orientation of an object from the rotation of the object.
    Use this to find the direction of cars: forward, right, up.
    It can also be used to find relative locations.
    """

    def __init__(self, front: Vector3, top: Vector3):
        self.front = front
        self.top = top

