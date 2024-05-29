from matplotlib import pyplot as plt
import sympy as sp

from Section_Point import Section_Point
from Section import Section
from Axis_Point import Axis_Point
from Support import Support
from Segment import Segment
from sympy import Eq, solve


segments = []
section_points = []
axis_points = []
# A list containing the objects which have an internal force
internal_forces_obj = []

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
    internal_forces_obj = list(filter(lambda x: x.support.name != "Free", axis_points))


# Checks if the problem is statically determined and returns false otherwise
def integrity_check(points):
    blocked_dof = 0
    for x_point in points:
        blocked_dof += x_point.degrees_of_freedom()
    if blocked_dof > 2:
        return False
    return True


def create_segments(points):
    previous_shear_force = 0  # This variable saves the shear force in the previous axis point
    previous_bending_moment = 0
    for i in range(len(points) - 1):
        segment = Segment(points[i], points[i + 1], points[i].distributed_force)
        segment.shear_function = segment.shear_function + previous_shear_force
        previous_shear_force = segment.shear_function_point_2()

        x = sp.symbols('x')
        segment.bending_function = sp.integrate(segment.shear_function,
                                                x) + segment.point_1.bending_moments + previous_bending_moment
        previous_bending_moment = segment.bending_moment_point_2()
        segments.append(segment)


# Calculates the sum of the shear forces and returns a simpy equation
def compute_shear_forces_sum(points, segments_y):
    shear_forces_sum = 0
    # To implement reduce
    for point_x in points:
        shear_forces_sum += point_x.concentrated_force
    for segment in segments_y:
        shear_forces_sum += segment.distributed_force * segment.length
    return Eq(sum(x.ya for x in points if x.ya is not None), -1 * shear_forces_sum)


# Calculates the sum of the bending moments and returns a simpy equation
def compute_moments_sum(points, segments_m):
    # Variable containing the sum of all the moments generated by the concentrated forces and the given bending moments
    moments_sum = 0
    # Variable containing the sum of the moments generated by the internal forces as well as the internal moments
    left_hand_side = 0
    # list containing the internal forces, internal_forces[0] will be the point where the moment is calculated
    internal_forces = list(filter(lambda x: x.support.name != "Free", axis_points))
    for point_x in points:
        if point_x.support.name != "Free":
            left_hand_side = point_x.ya * (internal_forces[0].x - point_x.x) + point_x.ma
        else:
            moments_sum += point_x.concentrated_force * (internal_forces[0].x - point_x.x) + point_x.bending_moments
    for segment in segments_m:
        if segment.distributed_force != 0:
            moments_sum += segment.distributed_force * segment.length * (internal_forces[0].x - segment.point_2.x
                                                                         + (segment.length / 2))
    return Eq(left_hand_side, -1 * moments_sum)


def plot_shear_diagram(list_of_segments):
    x_values = []
    y_values = []
    for segment in list_of_segments:
        x_values.append(segment.point_1.x)
        y_values.append(float(segment.shear_function_point_1()))
        x_values.append(segment.point_2.x)
        y_values.append(float(segment.shear_function_point_2()))

    # Plot the points using the lists
    plt.plot(x_values, y_values, 'g-')

    # Use fill_between to fill the area between the function and the x-axis
    plt.fill_between(x_values, y_values, color='skyblue', alpha=0.4)

    plt.title("Shear forces diagram")
    plt.xlabel("Length of the beam [mm]")
    plt.ylabel("Shear force [N]")
    plt.grid(True)
    plt.show()


def plot_bending_diagram(list_of_segments):
    x_values = []
    y_values = []
    for segment in list_of_segments:
        x_values.append(segment.point_1.x)
        y_values.append(float(segment.bending_moment_point_1()))
        x_values.append(segment.point_2.x)
        y_values.append(float(segment.bending_moment_point_2()))

    plt.plot(x_values, y_values, 'r-')
    plt.fill_between(x_values, y_values, color='red', alpha=0.3)

    plt.title("Bending moments diagram")
    plt.xlabel("Length of the beam [mm]")
    plt.ylabel("Bending moment [N]")
    plt.grid(True)
    plt.show()


if integrity_check(axis_points):
    create_segments(axis_points)
    section.display_section_properties()
    # section.display()
    section.plot_section()
    sum_y = compute_shear_forces_sum(axis_points, segments)
    sum_m = compute_moments_sum(axis_points, segments)
    sol = solve((sum_y, sum_m), [x.ya for x in internal_forces_obj] +
                [x.ma for x in internal_forces_obj if x.ma != 0])
    print(sum_y)
    print(sum_m)
    print(sol)

    for point in axis_points:
        point.set_ya(sol)
        # if point.name == "A":
        #     point.ya = sol[sp.Symbol("yA")]
        # elif point.name == "B":
        #     point.ya = sol[sp.Symbol("yB")]

    reaction = 0
    previous_bending_moment = 0
    for segment in segments:
        if segment.point_1.name.isalpha():
            reaction += segment.point_1.ya
        segment.shear_function += reaction

        x = sp.symbols('x')
        segment.bending_function = sp.integrate(segment.shear_function,
                                                x) + segment.point_1.bending_moments + previous_bending_moment
        previous_bending_moment = segment.bending_moment_point_2()

    plot_shear_diagram(segments)
    plot_bending_diagram(segments)

    # for segment in segments:
    #     print("segment:", segment.point_1.name, segment.point_2.name)
    #     print("Distributed force on segment: ", segment.distributed_force)
    #     print("Shear function: ", segment.shear_function)
    #     print("Shear force in Point 1:", segment.shear_function_point_1())
    #     print("Shear force in Point 2: ", segment.shear_function_point_2(), "\n")
    #     print("Bending function: ", segment.bending_function)
    #     print("Bending moment in Point 1:", segment.bending_moment_point_1())
    #     print("Bending moment in Point 2: ", segment.bending_moment_point_2(), "\n")

else:
    print("The problem is statically indeterminate")
