import numpy as np
from matplotlib import pyplot as plt
import sympy as sp

from Section_Point import Section_Point
from Section import Section
from Axis_Point import Axis_Point
from Support import Support
from Segment import Segment

import sys

segments = []
section_points = []
axis_points = []

with open("Problems/Exercise_01.txt", "r") as exercise:
    exercise_line = exercise.readlines()
    points_raw = exercise_line[0].strip().split(",")
    for point in points_raw:
        list_point = list(map(float, point.strip("()").split(";")))
        point_section = Section_Point(list_point[0], list_point[1])
        section_points.append(point_section)
    section = Section(section_points)
    for line in exercise_line[1:]:
        line_raw = line.split(";")
        support = Support(line_raw[2])
        axis_point = Axis_Point(line_raw[0], float(line_raw[1]), support,
                                float(line_raw[3]), float(line_raw[4]), float(line_raw[5]))
        axis_points.append(axis_point)


# Checks if the problem is statically determined and exists the program otherwise
def integrity_check(points):
    blocked_dof = 0
    for x_point in points:
        blocked_dof += 2 - x_point.degrees_of_freedom()
    if blocked_dof > 3:
        print("The problem is statically indeterminate")
        sys.exit()


def create_segments(points):
    previous_shear_force = 0  # This variable saves the shear force in the previous axis point
    for i in range(len(points) - 1):
        segment = Segment(points[i], points[i + 1], points[5].distributed_force)
        segment.s_function = segment.s_function + previous_shear_force
        previous_shear_force = segment.s_function_point_2()
        segments.append(segment)


def plot_shear_diagram(list_of_segments, beam):
#     # x_values = np.linspace(beam[0].x,beam[len(beam)-1].x)
#     for segment in list_of_segments:
#         x_values = np.linspace(segment.point_1.x,segment.point_2.x,100)
#         x = sp.symbols('x')
#         y_values = [segment.s_function.subs(x, val) for val in x_values]
#         x_values = np.append(x_values,segment.point_2.x)
#         y_values.append(segment)
#         plt.plot(x_values, y_values, 'g-')
    x_values = []
    y_values = []
    for segment in list_of_segments:

        x_values.append(segment.point_1.x)
        x = sp.symbols('x')
        y_values.append(segment.s_function_point_1())
        x_values.append(segment.point_2.x)
        y_values.append(segment.s_function_point_2())

    x_values.append(list_of_segments[len(list_of_segments)-1].point_2.x)
    y_values.append(0)
    plt.plot(x_values,y_values, 'g-')

    plt.title("Shear forces diagram")
    plt.xlabel("Length of the beam [mm]")
    plt.ylabel("Shear force [N]")

    plt.grid(True)

    plt.show()

integrity_check(axis_points)
create_segments(axis_points)
section.display()
section.plot_section()
for segment in segments:
    print("segment:", segment.point_1.name, segment.point_2.name)
    print("Distributed force on segment: ", segment.distributed_force)
    print("Shear function: ", segment.s_function)
    print("Shear force in Point 1:", segment.s_function_point_1())
    print("Shear force in Point 2: ", segment.s_function_point_2(), "\n")
plot_shear_diagram(segments, axis_points)
