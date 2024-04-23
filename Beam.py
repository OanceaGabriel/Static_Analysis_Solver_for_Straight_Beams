import numpy as np

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
        print("segment:", segment.point_1.name, segment.point_2.name)
        segment.s_function = segment.s_function + previous_shear_force
        previous_shear_force = segment.s_function_point_2()
        print(segment.s_function)
        segments.append(segment)


integrity_check(axis_points)
create_segments(axis_points)
section.display()
section.plot_section()
for segment in segments:
    print("segment:",segment.point_1.name,segment.point_2.name)
    print("Shear force in Point 1:",segment.s_function_point_1())
    print("Shear force in Point 2: ", segment.s_function_point_2())