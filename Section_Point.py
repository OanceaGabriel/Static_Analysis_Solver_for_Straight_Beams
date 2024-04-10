class Section_Point:
    y = None
    z = None

    def __init__(self, y, z):
        self.y = y
        self.z = z

    def display(self):
        print(f"y={self.y}, z={self.z}")
