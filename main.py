import pygame, sys
import os, sys
import config
import random
import numpy as np
from pathfinding import PathFinding
from copy import deepcopy
from threading import Thread
random.seed(config.SEED)
from objects import Button,DynamicLable,BoxLable,Node

TITLE = "A* Path Finder"
        

def get_tile_color(node):
   
    if node.walkable:
        tile_color = config.WALK_BLUE
    else:
        tile_color = config.UNWALK_BLACK

    if node.start_node:
        tile_color = config.START
        return tile_color
    elif node.target_node:
        tile_color = config.TARGET
        return tile_color
    
    if node.best_node:
        tile_color = config.BEST_GOLD
    elif node.selected:
        tile_color = config.SELECTED_GREEN
    elif node.taken:
        tile_color = config.TAKEN_RED
    
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
    for i in range(config.NUMBER_OF_COLOUMNS+1):
        new_height = round(i * config.BLOCK_H)
        new_width = round(i * config.BLOCK_W)
        pygame.draw.line(surface, config.GREY, (0, new_height), (config.SCREEN_WIDTH, new_height), 2)
        pygame.draw.line(surface, config.GREY, (new_width, 0), (new_width, config.SCREEN_HEIGHT), 2)

def game_loop(surface:pygame.Surface, map_rect:list,node_map:list):
    start_node = None
    target_node = None
    pathfinder = None
    pathfinder = PathFinding(deepcopy(node_map))
    finding_path = False

    start_button = Button(text="FIND",
                    x = config.SCREEN_WIDTH * 0.8 ,
                    y = config.SCREEN_HEIGHT+75//2 - 20,
                    width=100,height=40)
    
    clear_button = Button(text="CLEAR",
                    x = config.SCREEN_WIDTH * 0.6 ,
                    y = config.SCREEN_HEIGHT+75//2 - 20,
                    width=100,height=40)

    BoxLable("Exec Time: ").draw(surface)
    BoxLable("F Cost:",right_x=200).draw(surface)

    exec_time = "0 ms"
    total_cost = "0"   

    exec_time_label = DynamicLable(config.SCREEN_WIDTH * 0.05,
                                    config.SCREEN_HEIGHT + 40, 
                                    100,20)
    
    path_cost_label = DynamicLable(config.SCREEN_WIDTH * 0.35,
                                   config.SCREEN_HEIGHT + 40,
                                   100,20)

    while True:
        if finding_path:
            node_map,(exec_time,total_cost),end = pathfinder.mapqueue.get()
            if end:
                finding_path = False
                draw_map(surface, node_map)
                draw_grid(surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and map_rect.collidepoint(event.pos):
                if event.button == 1:
                    i,j = get_node_from_xy(event.pos)
                    node = node_map[i][j]
                    node.walkable = not node.walkable
                elif event.button == 3:
                    i,j = get_node_from_xy(event.pos)
                    if start_node is None:
                        start_node = node_map[i][j]
                        if not start_node.walkable:
                            start_node = None
                            continue
                        start_node.start_node = True
                    elif target_node is None:
                        target_node = node_map[i][j]
                        if not target_node.walkable:
                            target_node = None
                            continue
                        target_node.target_node = True
                        if pathfinder is not None:
                            pathfinder.set_start_target(start=start_node,
                                                        target=target_node)

        draw_map(surface, node_map)
        draw_grid(surface)
        
        #Dynamics labels
        exec_time_label.draw(surface,exec_time)       
        path_cost_label.draw(surface,total_cost)      

        if start_button.draw(surface):
            t = Thread(target=pathfinder.find_path, args=[node_map,config.SLEEP])
            t.start()
            finding_path = True
        
        if clear_button.draw(surface):
            node_map = pathfinder.reset()
            del pathfinder, start_node, target_node
            start_node = target_node = None
            exec_time ,total_cost = "0 ms","0"
            pathfinder = PathFinding(deepcopy(node_map))
            
        if finding_path:
            pathfinder.triggerq.put(True)
        pygame.display.update()

def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT+75))
    map_rect = pygame.Rect(0,0,config.SCREEN_HEIGHT,config.SCREEN_WIDTH)
    pygame.display.set_caption(TITLE)
    surface.fill(config.BACKGROUND)
    return surface,map_rect

def create_map():
    node_map = []
    for i in range(0,config.NUMBER_OF_ROWS):
        row_list = []
        for j in range(config.NUMBER_OF_COLOUMNS):
            node = Node(config.BLOCK_H,config.BLOCK_W,
                        grid_pos = [i,j],
                        center=np.array([j*config.BLOCK_W + config.BLOCK_W/2 ,
                                        i*config.BLOCK_H + config.BLOCK_H/2]),
                        walkable = random.random() > config.UNWALKABLE_RATIO)
            row_list.append(node)
        node_map.append(row_list)
    return node_map

def main():
    node_map = create_map()
    surface,map_rect = initialize_game()
    game_loop(surface, map_rect, node_map)

if __name__=="__main__":
    main()