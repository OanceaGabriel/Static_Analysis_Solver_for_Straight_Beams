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
            centroid_x += (-1) * (self.points_obj[i].y + self.points_obj[i + 1].y) * factor
            centroid_y += (-1) * (self.points_obj[i].z + self.points_obj[i + 1].z) * factor
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
        if abs(self.distance_from_centroid_to_fiber(self.find_lower_fiber())) < abs(self.distance_from_centroid_to_fiber(self.find_higher_fiber())):
            maximum = self.distance_from_centroid_to_fiber(self.find_higher_fiber())
        else:
            maximum = self.distance_from_centroid_to_fiber(self.find_lower_fiber())
        return maximum

    def y_max(self):
        if abs(self.distance_from_centroid_to_fiber(self.find_righter_fiber())) < abs(self.distance_from_centroid_to_fiber(self.find_lefter_fiber())):
            maximum = self.distance_from_centroid_to_fiber(self.find_righter_fiber())
        else:
            maximum = self.distance_from_centroid_to_fiber(self.find_lefter_fiber())
        return maximum

    def rigidity_module_Wy(self):
        return self.inertia_moment_y_calculation() / self.z_max()

    def rigidity_module_Wz(self):
        return self.inertia_moment_z_calculation() / self.y_max()

    def bending_stress_Sy_max(self, maximum_moment):
        return maximum_moment / self.rigidity_module_Wy()

    def find_lower_fiber(self):
        lower_fiber = 1000000
        for point in self.points_obj:
            if point.z < lower_fiber:
                lower_fiber = point.z
        return lower_fiber

    def find_higher_fiber(self):
        higher_fiber = -1000000
        for point in self.points_obj:
            if point.z > higher_fiber:
                higher_fiber = point.z
        return higher_fiber

    def find_lefter_fiber(self):
        find_lefter_fiber = -1000000
        for point in self.points_obj:
            if point.y < find_lefter_fiber:
                find_lefter_fiber = point.y
        return find_lefter_fiber

    def find_righter_fiber(self):
        find_righter_fiber = -1000000
        for point in self.points_obj:
            if point.y > find_righter_fiber:
                find_righter_fiber = point.y
        return find_righter_fiber

    def distance_from_centroid_to_fiber(self, z_coordinate):
        return abs(self.center_of_mass.z - z_coordinate)

    def bending_stress_in_lower_fiber(self, maximum_moment):
        return (maximum_moment * self.distance_from_centroid_to_fiber(
            self.find_lower_fiber())) / self.inertia_moment_y_calculation()

    def bending_stress_in_higher_fiber(self, maximum_moment):
        return (maximum_moment * self.distance_from_centroid_to_fiber(
            self.find_higher_fiber())) / self.inertia_moment_y_calculation()

    def __init__(self, points):
        self.points_obj = points
        for point in self.points_obj:
            point_tupple = (point.y, point.z)
            self.point_list.append(point_tupple)
        self.area = self.area_calculation()
        self.center_of_mass = self.center_calculation()

    # Displays center of mass and area of the section
    def display_section_properties(self, maximum_moment):
        self.center_of_mass.display()
        print(self.area)
        print("Iy= ", self.inertia_moment_y_calculation())
        print("Iz= ", self.inertia_moment_z_calculation())
        print("Izy= ", self.inertia_moment_zy_calculation())
        print("Wz = ", self.rigidity_module_Wy())
        print("Sigma_max = ", self.bending_stress_Sy_max(maximum_moment))
        print("z_max = ", self.z_max())
        print("Bending stress in lower fiber (z = ", self.find_lower_fiber(), ") = ",
              self.bending_stress_in_lower_fiber(maximum_moment))
        print("Bending stress in higher fiber (z = ", self.find_higher_fiber(), ")= ",
              self.bending_stress_in_higher_fiber(maximum_moment))

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
