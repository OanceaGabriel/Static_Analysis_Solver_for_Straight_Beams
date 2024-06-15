class Support:
    __name = None
    __dof = None
    #DOF represents the blocked degrees of freedom, examples bellow:
    #Support types are:
    #Fixed support(DOF = 2)/Incastrare
    #Roller support(DOF = 1, Rotation, horizontal is not taken into account)/Reazem
    #Pinned support(DOF = 1 Rotation)/Articulatie
    #No support(DOF = 0)

    def __init__(self, support):
        self.__name = support
        if support == "Fixed":
            self.__dof = 2
        elif support == "Pinned":
            self.__dof = 1
        elif support == "Roller":
            self.__dof = 1
        else:
            self.__dof = 0

    def get_name(self):
        return self.__name

    def get_dof(self):
        return self.__dof
