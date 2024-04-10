from Section_Point import Section_Point
from Section import Section
print("Hello World")

with open("Problems/Exercise_01.txt", "r") as exercise:
    section_points = []
    exercise_line = exercise.readlines()
    points_raw = exercise_line[0].strip("[]").split(",")
    for point in points_raw:
        list_point = list(map(float, (point.strip("()").split(";"))))
        point_section = Section_Point(list_point[0], list_point[1])
        section_points.append(point_section)
    section = Section(section_points)

section.display()
