import sympy as sp
from sympy import symbols


class Axis_Point:
    # The label of the point (eg: A, B, 1)
    __name = None
    # x represents the distance along the beam where the point is placed
    __x = None
    # the container for every force present in this point
    __concentrated_force = None
    # the container for every bending moment present in this point
    __bending_moments = None
    # Support object
    __support = None
    #Distributed force, to be given to the segment
    __distributed_force = None
    #The internal shear force and bending moment
    __ya = 0
    __ma = 0

    def __init__(self, name, x, support=None, concentrated_force=None, bending_moment=None, distributed_force=None):
        self.__name = name
        self.__x = x
        self.__concentrated_force = concentrated_force
        self.__bending_moments = bending_moment
        self.__support = support
        self.__distributed_force = distributed_force
        if self.__support.get_name() == "Pinned" or self.__support.get_name() == "Roller":
            self.__ya = symbols("y" + self.__name)
            self.__ma = 0
        elif self.__support.get_name() == "Fixed":
            self.__ya = symbols("y" + self.__name)
            self.__ma = symbols('ma' + self.__name)

    def degrees_of_freedom(self):
        return self.__support.get_dof()

    def set_ya(self, sol):
        if self.__name.isalpha():
            self.__ya = sol[sp.Symbol("y" + self.__name)]

    def set_name(self, name):
        self.__name = name

    def get_ya(self):
        return self.__ya

    def get_name(self):
        return self.__name

    def get_ma(self):
        return self.__ma

    def get_x(self):
        return self.__x

    def get_concentrated_force(self):
        return self.__concentrated_force

    def get_bending_moments(self):
        return self.__bending_moments

    def get_support(self):
        return self.__support

    def get_distributed_force(self):
        return self.__distributed_force

