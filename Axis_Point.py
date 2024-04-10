from Section import Section


class Axis_Point:
    # x represents the distance along the beam where the point is placed
    x = None
    # the container for every load present in this point (ex: Force, Bending Moment etc.)
    forces = []
    bending_moments = []

    def __init__(self, x, forces=[], bending_moments=[]):
        self.x = x
        self.forces = forces
        self.bending_moments = bending_moments
