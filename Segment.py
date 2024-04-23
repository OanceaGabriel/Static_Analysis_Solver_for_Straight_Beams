# This class is used for easier manipulation of the beam's segments

from Axis_Point import Axis_Point
import sympy as sp


class Segment:
    point_1 = Axis_Point
    point_2 = Axis_Point
    length = None
    distributed_force = 0
    point_mid = None
    s_function = None

    def __init__(self, point_1, point_2, distributed_force=0):
        self.point_1 = point_1
        self.point_2 = point_2
        self.length = self.point_2.x - self.point_1.x
        self.point_mid = self.point_1.x + self.length / 2
        if point_1.distributed_force != 0 and point_2.distributed_force != 0:
            self.distributed_force = distributed_force
            x = sp.symbols('x')
            self.s_function = (self.distributed_force / self.length) * x
        else:
            self.s_function = self.point_1.concentrated_forces

    # The function used to plot the shear forces graph
    def s_function_point_2(self):
        x_value = self.point_2.x
        x = sp.symbols('x')
        return self.s_function.subs(x, x_value)

    def s_function_point_1(self):
        x_value = self.point_1.x
        x = sp.symbols('x')
        return self.s_function.subs(x, x_value)

    # the function used to plot the bending moments graph
    def bm_function(self):
        pass
