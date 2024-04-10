from Section import Section


class Axis_Point:
    # x represents the distance along the beam where the point is placed
    x = None
    # the container for every load present in this point (ex: Force, Bending Moment etc.)
    loads = []

    def __init__(self, x, loads):
        self.x = x
        self.loads = loads
