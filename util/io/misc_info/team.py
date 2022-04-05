from enum import Enum


class Team(Enum):
    BLUE = 0
    ORANGE = 1

    @staticmethod
    def idToTeam(id: int):
        if id == 0:
            return Team.BLUE
        return Team.ORANGE
