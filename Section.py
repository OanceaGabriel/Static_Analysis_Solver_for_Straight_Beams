from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from Section_Point import Section_Point


class Section:
    points_obj = []
    point_list = []
    center_of_mass = None
    area = None

    # Calculates the section area
    def area_calculation(self):
        area = 0
        for i in range(len(self.points_obj) - 1):
            area += self.points_obj[i].y * self.points_obj[i + 1].z - self.points_obj[i + 1].y * self.points_obj[i].z
        self.area = abs(area) / 2
        return abs(area) / 2

    # Calculates the center of mass
    def center_calculation(self):
        centroid_x = 0
        centroid_y = 0
        for i in range(len(self.points_obj) - 1):
            factor = self.points_obj[i].y * self.points_obj[i + 1].z - self.points_obj[i + 1].y * self.points_obj[i].z
            centroid_x += (self.points_obj[i].y + self.points_obj[i + 1].y) * factor
            centroid_y += (self.points_obj[i].z + self.points_obj[i + 1].z) * factor
        centroid_x /= (6 * self.area)
        centroid_y /= (6 * self.area)
        center_of_gravity = Section_Point(centroid_x, centroid_y)
        return center_of_gravity

    def __init__(self, points):
        self.points_obj = points
        for point in self.points_obj:
            point_tupple = (point.y, point.z)
            self.point_list.append(point_tupple)
        self.area = self.area_calculation()
        self.center_of_mass = self.center_calculation()

    # Displays center of mass and area of the section
    def display(self):
        self.center_of_mass.display()
        print(self.area)

    def plot_section(self):
        fig, axis = plt.subplots()
        axis.set_aspect('equal', 'box')

        # Adds the polygon as a patch in the plot axis
        poly_patch = Polygon(self.point_list, closed=True, edgecolor='r', linewidth=2)
        axis.add_patch(poly_patch)

        # Sets the axis limits
        min_x = min(p[0] for p in self.point_list)
        max_x = max(p[0] for p in self.point_list)
        min_y = min(p[1] for p in self.point_list)
        max_y = max(p[1] for p in self.point_list)
        axis.set_xlim(min_x - 1, max_x + 1)
        axis.set_ylim(min_y - 1, max_y + 1)

        # Axis labels
        axis.set_xlabel('Y')
        axis.set_ylabel('Z')

        # Shows the plot
        plt.grid(True)
        plt.title("Section")
        plt.show()
