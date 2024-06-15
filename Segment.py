# This class is used for easier manipulation of the beam's segments
from sympy import integrate
import sympy as sp
from Axis_Point import Axis_Point


class Segment:
    point_1 = Axis_Point
    point_2 = Axis_Point
    length = None
    distributed_force = 0
    point_mid = None
    shear_function = None
    bending_function = None

    def __init__(self, point_1, point_2, distributed_force=0):
        self.__point_1 = point_1
        self.__point_2 = point_2
        self.__name = point_1.get_name() + point_2.get_name()
        self.__length = self.__point_2.get_x() - self.__point_1.get_x()
        self.__point_mid = self.__point_1.get_x() + self.__length / 2

        x = sp.symbols('x')
        if point_1.get_distributed_force() != 0 and point_2.get_distributed_force() != 0:
            self.__distributed_force = distributed_force
            self.__shear_function = self.__distributed_force * x + self.__point_1.get_ya()
        else:
            self.__shear_function = sp.sympify(0 * x + self.__point_1.get_concentrated_force())

        self.__bending_function = sp.integrate(self.__shear_function, x)

    # The function used to plot the shear forces graph
    def shear_function_point_2(self):
        x_value = self.__length
        x = sp.symbols('x')
        return self.__shear_function.subs(x, x_value)

    def shear_function_point_1(self):
        x_value = 0
        x = sp.symbols('x')
        return self.__shear_function.subs(x, x_value)

    def bending_moment_point_1(self):
        x_value = 0
        x = sp.symbols('x')
        return self.__bending_function.subs(x, x_value)

    def bending_moment_point_2(self):
        x_value = self.__length
        x = sp.symbols('x')
        return self.__bending_function.subs(x, x_value)

    def maximum_bending_moment(self):
        if abs(self.bending_moment_point_1()) > abs(self.bending_moment_point_2()):
            mbm = self.bending_moment_point_1()
        else:
            mbm = self.bending_moment_point_2()
        return mbm

    def get_distributed_force(self):
        return self.__distributed_force

    def get_point_1(self):
        return self.__point_1

    def get_point_2(self):
        return self.__point_2

    def get_length(self):
        return self.__length

    def get_shear_function(self):
        return self.__shear_function

    def set_shear_function(self, shear_function):
        self.__shear_function = shear_function

    def get_bending_function(self):
        return self.__bending_function

    def set_bending_function(self, bending_function):
        self.__bending_function = bending_function
