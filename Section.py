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
            centroid_x += (-1)*(self.points_obj[i].y + self.points_obj[i + 1].y) * factor
            centroid_y += (-1)*(self.points_obj[i].z + self.points_obj[i + 1].z) * factor
        centroid_x /= (6 * self.area)
        centroid_y /= (6 * self.area)
        center_of_gravity = Section_Point(centroid_x, centroid_y)
        return center_of_gravity

    def inertia_moment_y_calculation(self):  # This algorithm uses Shoelace formula
        inertia_moment_y = 0.0
        centroid_y = self.center_of_mass.y
        centroid_z = self.center_of_mass.z

        for i in range(len(self.points_obj)):
            z1, y1 = self.points_obj[i].z - centroid_z, self.points_obj[i].y - centroid_y
            z2, y2 = self.points_obj[(i + 1) % len(self.points_obj)].z - centroid_z, self.points_obj[
                (i + 1) % len(self.points_obj)].y - centroid_y

            product_y = z1 * y2 - z2 * y1

            inertia_moment_y += (z1 ** 2 + z1 * z2 + z2 ** 2) * product_y

        inertia_moment_y /= 12

        return inertia_moment_y

    def inertia_moment_z_calculation(self):  # This algorithm uses Shoelace formula
        inertia_moment_z = 0.0
        centroid_y = self.center_of_mass.y
        centroid_z = self.center_of_mass.z

        for i in range(len(self.points_obj)):
            z1, y1 = self.points_obj[i].z - centroid_z, self.points_obj[i].y - centroid_y
            z2, y2 = self.points_obj[(i + 1) % len(self.points_obj)].z - centroid_z, self.points_obj[
                (i + 1) % len(self.points_obj)].y - centroid_y
            product_z = y2 * z1 - y1 * z2

            inertia_moment_z += (y1 ** 2 + y1 * y2 + y2 ** 2) * product_z
        inertia_moment_z /= 12

        return inertia_moment_z

    def inertia_moment_zy_calculation(self):  # This algorithm uses Shoelace formula
        inertia_moment_zy = 0.0
        centroid_y = self.center_of_mass.y
        centroid_z = self.center_of_mass.z

        for i in range(len(self.points_obj)):
            z1, y1 = self.points_obj[i].z - centroid_z, self.points_obj[i].y - centroid_y
            z2, y2 = self.points_obj[(i + 1) % len(self.points_obj)].z - centroid_z, self.points_obj[
                (i + 1) % len(self.points_obj)].y - centroid_y
            product_z = y2 * z1 - y1 * z2

            inertia_moment_zy += (z1 * y2 + 2 * z1 * y1 + 2 * z2 * y2 + z2 * y1) * product_z
        inertia_moment_zy /= 24

        return inertia_moment_zy

    def z_max(self):
        max = 0
        for section_point in self.points_obj:
            if abs(max) < abs(section_point.z):
                max = section_point.z
        return max - self.center_of_mass.y

    def y_max(self):
        max = 0
        for section_point in self.points_obj:
            if abs(max) < abs(section_point.y):
                max = section_point.y
        return max - self.center_of_mass.z

    def rigidity_module_Wy(self):
        return self.inertia_moment_y_calculation() / self.z_max()

    def rigidity_module_Wz(self):
        return self.inertia_moment_z_calculation() / self.y_max()


    def __init__(self, points):
        self.points_obj = points
        for point in self.points_obj:
            point_tupple = (point.y, point.z)
            self.point_list.append(point_tupple)
        self.area = self.area_calculation()
        self.center_of_mass = self.center_calculation()

    # Displays center of mass and area of the section
    def display_section_properties(self):
        self.center_of_mass.display()
        print(self.area)
        print("Iy= ", self.inertia_moment_y_calculation())
        print("Iz= ", self.inertia_moment_z_calculation())
        print("Izy= ", self.inertia_moment_zy_calculation())

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
