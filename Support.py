class Support:
    name = None
    dof = None

    # Support types are:
    # Fixed support(DOF = 0)/Incastrare
    # Roller support(DOF = 1, horizontal and rotation)/Reazem
    # Pinned support(DOF = 2 Rotation)/Articulatie
    # No support(DOF = 3)

    def __init__(self, support):
        self.name = support
        if support == "Fixed":
            self.dof = 2
        elif support == "Pinned":
            self.dof = 1
        elif support == "Roller":
            self.dof = 1
        else:
            self.dof = 2
