# from Section import Section


class Axis_Point:
    # The label of the point (eg: A, B, 1)
    name = None
    # x represents the distance along the beam where the point is placed
    x = None
    # the container for every force present in this point
    concentrated_forces = []
    # the container for every bending moment present in this point
    bending_moments = []
    # Support object
    support = None
    # Distributed force, to be given to the segment
    distributed_force = None

    def __init__(self, name, x, support=None, concentrated_force=None, bending_moment=None, distributed_force=None):
        self.name = name
        self.x = x
        self.concentrated_forces = concentrated_force
        self.bending_moments = bending_moment
        self.support = support
        self.distributed_force = distributed_force

    def degrees_of_freedom(self):
        return self.support.dof
