class Support:
    name = None
    dof = None
    #Support types are:
    #Fixed support(DOF = 0)
    #Pinned support(DOF = 1 Rotation)
    #Roller support(DOF = 2, horizontal and rotation)
    #No support(DOF = 3)

    def __init__(self, support):
        self.name = support
        if support == "Fixed":
            self.dof = 0
        elif support == "Pinned":
            self.dof = 1
        elif support == "Roller":
            self.dof = 1
        else:
            self.dof = 2
