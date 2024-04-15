#This class is used for easier manipulation of the beam's segments

class Segment:
    point_1 = None
    point_2 = None
    length = None
    distributed_force = 0

    def __init__(self, point_1, point_2, distributed_force=0):
        self.point_1 = point_1
        self.point_2 = point_2
        self.length = self.point_2.x - self.point_1.x
        if point_1.distributed_force != 0 and point_2.distributed_force != 0:
            self.distributed_force = distributed_force

    #The function used to plot the shear forces graph
    def s_function(self):
        pass

    #the function used to plot the bending moments graph
    def bm_function(self):
        pass


