#from Section import Section


class Axis_Point:
    # x represents the distance along the beam where the point is placed
    x = None
    # the container for every force present in this point
    concentrated_forces = []
    # the container for every bending moment present in this point
    bending_moments = []
    # Support object
    support = None

    def __init__(self, x, concentrated_forces=None, bending_moments=None, support=None):
        self.x = x
        self.concentrated_forces = concentrated_forces
        self.bending_moments = bending_moments
        self.support = support

    def degrees_of_freedom(self):
        return self.support.dof
