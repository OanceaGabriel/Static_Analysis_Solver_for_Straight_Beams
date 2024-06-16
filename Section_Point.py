class Section_Point:
    __y = None
    __z = None

    def __init__(self, y, z):
        self.__y = y
        self.__z = z

    def display(self):
        print(f"Center of mass coordinates y={self.__y} mm, z={self.__z} mm")

    def get_y(self):
        return self.__y

    def get_z(self):
        return self.__z
