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
        self.point_1 = point_1
        self.point_2 = point_2
        self.length = self.point_2.x - self.point_1.x
        self.point_mid = self.point_1.x + self.length / 2

        x = sp.symbols('x')
        if point_1.distributed_force != 0 and point_2.distributed_force != 0:
            self.distributed_force = distributed_force
            self.shear_function = self.distributed_force * x
        else:
            self.shear_function = sp.sympify(0*x + self.point_1.concentrated_force)

        self.bending_function = sp.integrate(self.shear_function, x)

    # The function used to plot the shear forces graph
    def shear_function_point_2(self):
        x_value = self.length
        x = sp.symbols('x')
        return self.shear_function.subs(x, x_value)

    def shear_function_point_1(self):
        x_value = 0
        x = sp.symbols('x')
        return self.shear_function.subs(x, x_value)

    def bending_moment_point_1(self):
        x_value = 0
        x = sp.symbols('x')
        return self.bending_function.subs(x, x_value)

    def bending_moment_point_2(self):
        x_value = self.length
        x = sp.symbols('x')
        return self.bending_function.subs(x, x_value)
