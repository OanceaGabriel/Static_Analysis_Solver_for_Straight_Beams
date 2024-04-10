from Section_Point import Point
#from matplotlib.patches import Polygon


class Section:
    points = []
    center_of_mass = None

    def area(self):
        area = 0
        for i in range(len(self.points) - 1):
            area += self.points[i].y * self.points[i + 1].z - self.points[i + 1].y * self.points[i].z
        return abs(area) / 2

    def center_calculation(self):
        area = self.area()
        centroid_x = 0
        centroid_y = 0
        for i in range(len(self.points) - 1):
            factor = self.points[i].y * self.points[i + 1].z - self.points[i + 1].y * self.points[i].z
            centroid_x += (self.points[i].y + self.points[i + 1].y) * factor
            centroid_y += (self.points[i].z + self.points[i + 1].z) * factor
        centroid_x /= (6 * area)
        centroid_y /= (6 * area)
        center_of_gravity = Point(centroid_x, centroid_y)
        return center_of_gravity

    def __init__(self, points):
        self.points = points
        self.center_of_mass = self.center_calculation()
