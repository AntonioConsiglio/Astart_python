import pygame, sys
import os, sys
import config
import random
import numpy as np
from pathfinding import PathFinding
from copy import deepcopy

def get_tile_color(node):
   
    if node.walkable:
        tile_color = config.WALK_BLUE
    else:
        tile_color = config.UNWALK_BLACK

    if node.start_node:
        tile_color = config.START
    elif node.target_node:
        tile_color = config.TARGET
    
    if node.best_node:
        tile_color = config.BEST_GOLD
    
    return tile_color

def get_node_from_xy(pos):
    i = pos[1]//config.BLOCK_H 
    j = pos[0]//config.BLOCK_H 
    return [i,j]

def draw_map(surface, node_map):
    for row, row_nodes in enumerate(node_map):
        for node in row_nodes:
            node:Node
            # print("{},{}: {}".format(i, j, tile_contents))
            myrect = pygame.Rect(*node.topleft,node.h,node.w)
            pygame.draw.rect(surface, get_tile_color(node), myrect)

def draw_grid(surface):
    for i in range(config.NUMBER_OF_COLOUMNS):
        new_height = round(i * config.BLOCK_H)
        new_width = round(i * config.BLOCK_W)
        pygame.draw.line(surface, config.GREY, (0, new_height), (config.SCREEN_WIDTH, new_height), 2)
        pygame.draw.line(surface, config.GREY, (new_width, 0), (new_width, config.SCREEN_HEIGHT), 2)

def game_loop(surface, node_map:list):
    start_node = None
    pathfinder = None
    pathfinder = PathFinding(deepcopy(node_map))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    i,j = get_node_from_xy(event.pos)
                    node = node_map[i][j]
                    node.walkable = not node.walkable
                elif event.button == 3:
                    i,j = get_node_from_xy(event.pos)
                    if start_node is None:
                        start_node = node_map[i][j]
                        start_node.start_node = True
                    else:
                        target_node = node_map[i][j]
                        target_node.target_node = True
                        if pathfinder is not None and pathfinder.best_path is None:
                            pathfinder.set_start_target(start=start_node,
                                                        target=target_node)
                        else:
                            node_map = pathfinder.reset()
                            del pathfinder
                            del start_node
                            start_node = None
                            pathfinder = PathFinding(deepcopy(node_map))

                elif event.button == 2:
                    node_map = pathfinder.find_path(node_map)
                    

                
        draw_map(surface, node_map)
        draw_grid(surface)
        pygame.display.update()

def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption(config.TITLE)
    surface.fill(config.WALK_BLUE)
    return surface

class Node():
    def __init__(self,h,w,grid_pos,center,walkable):
        self.h ,self.w = h, w
        self.grid_pos = grid_pos
        self.center = center
        self.walkable = walkable
        self.topleft = [v for v in self.center - np.array([w/2,h/2])]
        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

        self.start_node = False
        self.target_node = False
        
        self.best_node = False
    
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
            return 1.47*dy + 1*dx

        return 1.47*dx + 1*dy

    def calculate_hcost(self,target):

        dx = abs(self.col - target.col)
        dy = abs(self.row - target.row)

        if dx > dy:
            self.h_cost = 1.47*dy + 1*(dx-dy)
        else:
            self.h_cost = 1.47*dx + 1*(dy-dx)
    
    def __eq__(self,node) -> bool:
        return all(np.equal(self.center,node.center))

def create_map():
    node_map = []
    for i in range(0,config.NUMBER_OF_ROWS):
        row_list = []
        for j in range(config.NUMBER_OF_COLOUMNS):
            node = Node(config.BLOCK_H,config.BLOCK_W,
                        grid_pos = [i,j],
                        center=np.array([j*config.BLOCK_W + config.BLOCK_W/2 ,
                                        i*config.BLOCK_H + config.BLOCK_H/2]),
                        walkable = random.random() > 0.15)
            row_list.append(node)
        node_map.append(row_list)
    return node_map

def main():
    node_map = create_map()
    surface = initialize_game()
    game_loop(surface, node_map)

if __name__=="__main__":
    main()