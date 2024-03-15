import config 
from copy import deepcopy
from queue import Queue as Q
import time
class PathFinding():

    def __init__(self,node_map,):
        self.open_node = []
        self.used_node = []

        self.node_map = node_map.copy()
        self.best_path = None

        self.mapqueue = Q(10)
        self.triggerq = Q(1)

    def set_start_target(self,start,target):
        self.start_node = start
        self.target_node = target

    def find_path(self,node_map,sleep:float=0):
        self.open_node.append(self.start_node) #insert the first node where we start
        step = 0
        while len(self.open_node) > 0:
            step+=1
            if step > 1:
                self.mapqueue.put([node_map,False])
                _ = self.triggerq.get()
                time.sleep(sleep)
            #print(f"{step=}")
            curr_node = self.open_node[0] #current position Node
            # while in the first step, this is skipped because the self.open_node is len = 1
            # During this step we investigate which neigh will be the next node to became curr node
            # The selection is based on the best f_cost (sum of h + g cost)
            for j in range(1,len(self.open_node)):
                if (self.open_node[j].f_cost < curr_node.f_cost or 
                    (self.open_node[j].f_cost == curr_node.f_cost and 
                     self.open_node[j].h_cost < curr_node.h_cost)):
                    curr_node = self.open_node[j]
            # remove open node and add it in the used node list
            if not curr_node == self.start_node:
                curr_node.selected = True
            self.open_node.remove(curr_node)
            self.used_node.append(curr_node)
            # If the curr node is equal to the target we have arrived to the target
            if curr_node == self.target_node:
                # curr_node.target_node = True
                print("Get best path")
                self.get_best_path(curr_node)
                self.best_path = node_map
                self.mapqueue.put([node_map,True])
                return
            # Starting from the curr node we investigate to the neigh to check where to go
            # We calculate 2 distances. One is the distance from the curr to the next node (g cost), 
            # the other is the distance from the next node to the target node (h cost)
            for i,j in self.get_neighbours(curr_node):
                if self.check_limits(i,j,curr_node):
                    continue
                neigh_node = node_map[i][j]
                if not neigh_node.walkable or neigh_node in self.used_node:
                    continue

                cost2neigh = curr_node.g_cost + curr_node.calculate_gcost(neigh_node)
                if cost2neigh < neigh_node.g_cost or neigh_node not in self.open_node:
                    neigh_node.g_cost = cost2neigh
                    neigh_node.calculate_hcost(self.target_node)
                    neigh_node.parent = curr_node

                    if neigh_node not in self.open_node:
                        neigh_node.taken = True
                        self.open_node.append(neigh_node)

        print("No more open_node Nodes")
        self.mapqueue.put([node_map,True])
        self.best_path = node_map
        return 
    
    def get_neighbours(self,node):
        interval = 1
        istart = node.row - interval
        if istart < 0 : istart = 0
        jstart = node.col - interval
        if jstart < 0 : jstart = 0

        for i in range(istart,node.row+interval+1):
            for j in range(jstart,node.col+interval+1):
                yield i,j 
    
    def get_best_path(self,curr_node):
        while( curr_node.parent is not None):
            if not curr_node == self.target_node:
                curr_node.best_node = True
            curr_node = curr_node.parent
        return

    def reset(self,):
        return deepcopy(self.node_map)

    def check_limits(self,i,j,curr_node):
        if i == curr_node.row and j == curr_node.col:
            return True
        if i >= config.NUMBER_OF_ROWS or j >= config.NUMBER_OF_ROWS:
            return True
        return False
