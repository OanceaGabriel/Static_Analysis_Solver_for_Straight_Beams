class Support:
    name = None
    dof = None
    #DOF represents the blocked degrees of freedom, examples bellow:
    #Support types are:
    #Fixed support(DOF = 2)/Incastrare
    #Roller support(DOF = 1, Rotation, horizontal is not taken into account)/Reazem
    #Pinned support(DOF = 1 Rotation)/Articulatie
    #No support(DOF = 0)

    def __init__(self, support):
        self.name = support
        if support == "Fixed":
            self.dof = 2
        elif support == "Pinned":
            self.dof = 1
        elif support == "Roller":
            self.dof = 1
        else:
            self.dof = 0
