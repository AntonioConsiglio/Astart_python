import numpy as np
class Node():
    def __init__(self,h,w,grid_pos,center,walkable):
        self.h ,self.w = h, w
        self.grid_pos = grid_pos
        self.center = tuple([c for c in center])
        self.walkable = walkable
        self.topleft = [v for v in center - np.array([w/2,h/2])]
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

        self.start_node = False
        self.target_node = False
        
        self.taken = False
        self.best_node = False
        self.selected = False
    
    @property
    def f_cost(self):
        return self.g_cost+self.h_cost
    
    @property
    def row(self):
        return self.grid_pos[0]

    @property
    def col(self):
        return self.grid_pos[1]    

    def calculate_gcost(self,dest):
        dx = abs(self.col - dest.col)
        dy = abs(self.row - dest.row)

        if dx > dy:
            return 1.414*dy + 1*(dx-dy)

        return 1.414*dx + 1*(dy-dx)

    def calculate_hcost(self,target):

        dx = abs(self.col - target.col)
        dy = abs(self.row - target.row)

        if dx > dy:
            self.h_cost = 1.414*dy + 1*(dx-dy)
        else:
            self.h_cost = 1.414*dx + 1*(dy-dx)
    
    def __eq__(self,node) -> bool:
        return self.center == node.center
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost
    
    def __hash__(self):
        return hash(self.center)
