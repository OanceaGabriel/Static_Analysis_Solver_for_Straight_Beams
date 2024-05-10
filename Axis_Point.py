from sympy import symbols


class Axis_Point:
    # The label of the point (eg: A, B, 1)
    name = None
    # x represents the distance along the beam where the point is placed
    x = None
    # the container for every force present in this point
    concentrated_force = None
    # the container for every bending moment present in this point
    bending_moments = None
    # Support object
    support = None
    #Distributed force, to be given to the segment
    distributed_force = None
    #The internal shear force and bending moment
    ya = 0
    ma = 0

    def __init__(self, name, x, support=None, concentrated_force=None, bending_moment=None, distributed_force=None):
        self.name = name
        self.x = x
        self.concentrated_force = concentrated_force
        self.bending_moments = bending_moment
        self.support = support
        self.distributed_force = distributed_force
        if self.support.name == "Pinned" or self.support.name == "Roller":
            self.ya = symbols("y" + self.name)
            self.ma = 0
        elif self.support.name == "Fixed":
            self.ya = symbols("y" + self.name)
            self.ma = symbols('ma' + self.name)

    def degrees_of_freedom(self):
        return self.support.dof
