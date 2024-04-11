from Section_Point import Section_Point
from Section import Section
from Axis_Point import Axis_Point

import sys

with open("Problems/Exercise_01.txt", "r") as exercise:
    section_points = []
    axis_points = []
    exercise_line = exercise.readlines()
    points_raw = exercise_line[0].split(",")
    for point in points_raw:
        list_point = list(map(float, point.strip("()").split(";")))
        point_section = Section_Point(list_point[0], list_point[1])
        section_points.append(point_section)
    section = Section(section_points)

# Checks if the problem is statically determined and exists the program otherwise
blocked_dof = 0
for x_point in axis_points:
    blocked_dof += x_point.support.degrees_of_freedom()
if blocked_dof > 3:
    print("The problem is statically indeterminate")
    sys.exit()

section.display()
section.plot_section()
