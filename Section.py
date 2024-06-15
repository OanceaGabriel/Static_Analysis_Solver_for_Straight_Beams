from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from Section_Point import Section_Point


class Section:
    __points_obj = []
    __point_list = []
    __center_of_mass = None
    __area = None

    # Calculates the section area
    def area_calculation(self):
        area = 0
        for i in range(len(self.__points_obj) - 1):
            area += self.__points_obj[i].get_y() * self.__points_obj[i + 1].get_z() - self.__points_obj[i + 1].get_y() * self.__points_obj[i].get_z()
        self.__area = abs(area) / 2
        return abs(area) / 2

    # Calculates the center of mass
    def center_calculation(self):
        centroid_x = 0
        centroid_y = 0
        for i in range(len(self.__points_obj) - 1):
            factor = self.__points_obj[i].get_y() * self.__points_obj[i + 1].get_z() - self.__points_obj[i + 1].get_y() * self.__points_obj[i].get_z()
            centroid_x += (-1) * (self.__points_obj[i].get_y() + self.__points_obj[i + 1].get_y()) * factor
            centroid_y += (-1) * (self.__points_obj[i].get_z() + self.__points_obj[i + 1].get_z()) * factor
        centroid_x /= (6 * self.__area)
        centroid_y /= (6 * self.__area)
        center_of_gravity = Section_Point(centroid_x, centroid_y)
        return center_of_gravity

    def inertia_moment_y_calculation(self):  # This algorithm uses Shoelace formula
        inertia_moment_y = 0.0
        centroid_y = self.__center_of_mass.get_y()
        centroid_z = self.__center_of_mass.get_z()

        for i in range(len(self.__points_obj)):
            z1, y1 = self.__points_obj[i].get_z() - centroid_z, self.__points_obj[i].get_y() - centroid_y
            z2, y2 = self.__points_obj[(i + 1) % len(self.__points_obj)].get_z() - centroid_z, self.__points_obj[
                (i + 1) % len(self.__points_obj)].get_y() - centroid_y

            product_y = z1 * y2 - z2 * y1

            inertia_moment_y += (z1 ** 2 + z1 * z2 + z2 ** 2) * product_y

        inertia_moment_y /= 12

        return inertia_moment_y

    def inertia_moment_z_calculation(self):  # This algorithm uses Shoelace formula
        inertia_moment_z = 0.0
        centroid_y = self.__center_of_mass.get_y()
        centroid_z = self.__center_of_mass.get_z()

        for i in range(len(self.__points_obj)):
            z1, y1 = self.__points_obj[i].get_z() - centroid_z, self.__points_obj[i].get_y() - centroid_y
            z2, y2 = self.__points_obj[(i + 1) % len(self.__points_obj)].get_z() - centroid_z, self.__points_obj[
                (i + 1) % len(self.__points_obj)].get_y() - centroid_y
            product_z = y2 * z1 - y1 * z2

            inertia_moment_z += (y1 ** 2 + y1 * y2 + y2 ** 2) * product_z
        inertia_moment_z /= 12

        return inertia_moment_z

    def inertia_moment_zy_calculation(self):  # This algorithm uses Shoelace formula
        inertia_moment_zy = 0.0
        centroid_y = self.__center_of_mass.get_y()
        centroid_z = self.__center_of_mass.get_z()

        for i in range(len(self.__points_obj)):
            z1, y1 = self.__points_obj[i].get_z() - centroid_z, self.__points_obj[i].get_y() - centroid_y
            z2, y2 = self.__points_obj[(i + 1) % len(self.__points_obj)].get_z() - centroid_z, self.__points_obj[
                (i + 1) % len(self.__points_obj)].get_y() - centroid_y
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
        for point in self.__points_obj:
            if point.get_z() < lower_fiber:
                lower_fiber = point.get_z()
        return lower_fiber

    def find_higher_fiber(self):
        higher_fiber = -1000000
        for point in self.__points_obj:
            if point.get_z() > higher_fiber:
                higher_fiber = point.get_z()
        return higher_fiber

    def find_lefter_fiber(self):
        find_lefter_fiber = -1000000
        for point in self.__points_obj:
            if point.__y < find_lefter_fiber:
                find_lefter_fiber = point.__y
        return find_lefter_fiber

    def find_righter_fiber(self):
        find_righter_fiber = -1000000
        for point in self.__points_obj:
            if point.__y > find_righter_fiber:
                find_righter_fiber = point.__y
        return find_righter_fiber

    def distance_from_centroid_to_fiber(self, z_coordinate):
        return abs(self.__center_of_mass.get_z() - z_coordinate)

    def bending_stress_in_lower_fiber(self, maximum_moment):
        return (maximum_moment * self.distance_from_centroid_to_fiber(
            self.find_lower_fiber())) / self.inertia_moment_y_calculation()

    def bending_stress_in_higher_fiber(self, maximum_moment):
        return (maximum_moment * self.distance_from_centroid_to_fiber(
            self.find_higher_fiber())) / self.inertia_moment_y_calculation()

    def __init__(self, points):
        self.__points_obj = points
        for point in self.__points_obj:
            point_tupple = (point.get_y(), point.get_z())
            self.__point_list.append(point_tupple)
        self.__area = self.area_calculation()
        self.__center_of_mass = self.center_calculation()

    # Displays center of mass and area of the section
    def display_section_properties(self, maximum_moment):
        self.__center_of_mass.display()
        print(self.__area)
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

    def plot_section(self, Y1,Y2):
        fig, axis = plt.subplots()
        axis.set_aspect('equal', 'box')

        # Adds the polygon as a patch in the plot axis
        poly_patch = Polygon(self.__point_list, closed=True, edgecolor='r', linewidth=2)
        axis.add_patch(poly_patch)

        # Sets the axis limits for the polygon
        min_x = min(p[0] for p in self.__point_list)
        max_x = max(p[0] for p in self.__point_list)
        min_y = min(p[1] for p in self.__point_list)
        max_y = max(p[1] for p in self.__point_list)

        # Calculate the shift amount
        shift_amount = 10  # shift amount of 5

        # Determine the Y position for the vertical line
        Y_vertical = max_x + shift_amount

        # Plotting the first-degree function (line) from points (Y1, Z1) and (Y2, Z2)
        Z1 = 13
        Z2 = 0

        # Adjusting the line to be shifted to the right of the polygon
        Y1_shifted = Y1 + Y_vertical
        Y2_shifted = Y_vertical - Y2

        # Plot the vertical line at Y = Y_vertical
        axis.plot([Y_vertical, Y_vertical], [min(min_y, Z2), max(max_y, Z1)], 'g-', linewidth=2)  # green dashed line

        # Plotting the shifted lines correctly
        axis.plot([Y1_shifted, Y2_shifted], [Z1, Z2], 'g-')  # blue line with dots

        # Add text for the first shifted point
        axis.text(Y1_shifted, Z1, f'σ={Y1:.2f}', color='black', fontsize=11, ha='right', va='bottom')

        # Add text for the second shifted point
        axis.text(Y2_shifted, Z2, f'σ={Y2:.2f}', color='black', fontsize=11, ha='left', va='top')

        # Fill the area between the vertical line and the shifted lines
        axis.fill_betweenx([Z1,Z2], Y_vertical, [Y1_shifted,Y2_shifted], color='green', alpha=0.2)  # fill segment 1

        # Set the axis limits to include both the polygon and the lines
        axis.set_xlim(min_x - 1, max_x + shift_amount + shift_amount)
        axis.set_ylim(min(min_y, Z2) - 1, max(max_y, Z1) + 1)

        # Axis labels
        axis.set_xlabel('Y')
        axis.set_ylabel('Z')

        # Show grid, title, and the plot
        plt.grid(True)
        plt.title("Section with Line and Filled Areas")
        plt.show()





