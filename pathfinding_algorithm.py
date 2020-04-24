###PATHFINDING ALGORITHM

#Explanation: This is a simple re-creation of the A* pathfinding algorithm. Running this program will load in a pygame menu
#with a board of white nodes. The white nodes can be walked on, the black nodes cannot. Use the left and right mouse button to set
#the different node types.

#Press 'T' to set the start point at the target location. Press the spacebar to set the destination. Once both are set,
#the program will automatically map out the shortest possible route between the two points. 

#Sometimes, this algorithm does not give the proper shortest path, and gives a slightly longer path. But in 90% of cases it works
#perfectly, and in the other 10% of cases it works decently. 

###INSTRUCTIONS: Press 'T' to place a starting point. Press 'SPACE' to set a destination. Once both are set, the program
#will automatically plot the shortest route.
#Click and hold the left mouse button to set impassable terrain (black). Hold down right mouse button to set it to passable
#terrain (white). Green terrain is twice as slow to traverse than white cells, but can still be traversed.

from my_library import *
import pygame as pg
import sys

type_color_dict = {1: (255, 255, 255), 0: (0, 0, 0), 2: (0, 255, 0)}
#Type 0 = passable, type 1 = impassable, type 2 = exploring, type 3 = player, type 4 = destination

class Node:
    def __init__(self, parent, i, j):
        self.parent = parent
        self.i = i
        self.j = j
        self.set_type(1)
        
    def __iter__(self):
        yield self.fcost
        
    def __gt__(self, other):
        return self.f_cost > other.f_cost or (self.f_cost == other.f_cost and self.h_cost > other.h_cost)
        
    def draw(self):
        #Draw Nodes
        pg.draw.rect(self.parent.screen, self.color, (self.i * self.parent.node_size, self.j * self.parent.node_size, self.parent.node_size, self.parent.node_size))
        #Draw borders
        pg.draw.rect(self.parent.screen, (100, 100, 100), (self.i * self.parent.node_size, self.j * self.parent.node_size, self.parent.node_size, self.parent.node_size), self.parent.node_border)
    
    def set_type(self, self_type):
        for _type, color in type_color_dict.items():
            if self_type == _type:
                self.type = _type
                self.color = color
                
    def get_pos(self):
        return (self.i * self.parent.node_size, self.j * self.parent.node_size)
                
class Destination:
    def __init__(self, parent):
        self.parent = parent
        self.size = self.parent.node_size
        self.color = (255, 0, 0)
        
    def create(self, xpos, ypos):
        self.xpos = xpos
        self.ypos= ypos
        
    def get_node(self):
        return self.parent.nodes[self.xpos // self.size][self.ypos // self.size]
        
    def draw(self, screen):
        if hasattr(self, 'xpos'):
            pg.draw.rect(screen, self.color, (self.xpos, self.ypos, self.size, self.size))
            
    def get_pos(self):
        return (self.xpos, self.ypos)
        
    
class Player(Destination):
    def __init__(self, parent):
        self.parent = parent
        self.size = self.parent.node_size
        self.color = (0, 0, 255)
        
    def move(self, x, y):
        i = self.xpos // self.size
        j = self.ypos // self.size
        if is_between(i, x - 1, x + 1) and is_between(j, y - 1, y + 1) and self.parent.nodes[x][y].type == 0:
            self.xpos = x * self.size
            self.ypos = y * self.size
            
class Pathfinding:
    def __init__(self, _map):
        self.map = _map
        self.map.agent = Player(self.map)
        self.map.agent.create(self.map.player.xpos, self.map.player.ypos)
        
        if hasattr(self.map.player, 'xpos') and hasattr(self.map.destination, 'xpos'):
            self.open = []
            self.closed = []
            self.run()
        
    def run(self):
        self.start = self.map.player.get_node()
        self.destination = self.map.destination.get_node()
        self.open.append(self.start)
        self.looping = True
        path = []
        ceiling_1 = self.map.width - 1; ceiling_2 = self.map.height - 1
        #Heap optimization was considered for getting the minimum nodes more quickly, but it was later discovered that
        #looking at only the neighbour nodes is faster, and works all the same.
        while len(self.open) and self.looping:
            current_node = self.open[0]; self.set_costs(current_node)
            for i in range(max(0, current_node.i + 2), min(ceiling_1, current_node.i - 1)):
                for j in range(max(0, current_node.j + 2), min(ceiling_2, current_node.j - 1)):
                    if self.map.nodes[i][j] < current_node:
                        current_node = self.map.nodes[i][j]
            self.open.remove(current_node)
            self.closed.append(current_node)
            
            if current_node is self.destination:
                path = self.retrace_path(self.start, self.destination)
                self.looping = False
                
            neighbours = self.get_node_neighbours(current_node)
            for neighbour in neighbours:
                if neighbour.type == 0 or neighbour in self.closed:
                    continue
                self.set_costs(neighbour)
                new_cost = current_node.g_cost + distance(current_node.get_pos(), neighbour.get_pos()) * neighbour.type
                if new_cost < neighbour.g_cost or neighbour not in self.open:
                    neighbour.g_cost = new_cost
                    neighbour.h_cost = distance(neighbour.get_pos(), self.destination.get_pos())
                    neighbour.previous = current_node
                    if neighbour not in self.open:
                        self.open.append(neighbour)
                    else:
                        self.update_costs(neighbour)
        
        #Draw the path in a slightly blue-ish color.                
        for node in path:
            node.color = (200, 200, 200)
            self.map.agent.move(node.i, node.j)
                
    def retrace_path(self, start, end):
        path = []
        current_node = end
        while current_node != start:
            current_node = current_node.previous
            path.append(current_node)
        path = path[::-1]
        return path
    
    def get_adjacent_neighbours(self, node):
        adjacent_neighbours = []
        adjacent_neighbours_coords = [(node.i - 1, node.j), (node.i + 1, node.j), (node.i, node.j - 1), (node.i, node.j + 1)]
        for coord in adjacent_neighbours_coords:
            if is_between(coord[0], 0, self.map.width - 1) and is_between(coord[1], 0, self.map.height - 1) and self.map.nodes[coord[0]][coord[1]].type != 0:
                adjacent_neighbours.append(self.map.nodes[coord[0]][coord[1]])
        return adjacent_neighbours
    
    def get_diagonal_neighbours(self, node):
        diagonal_neighbours = []
        diagonal_neighbours_coords = [(node.i - 1, node.j - 1), (node.i + 1, node.j + 1), (node.i + 1, node.j - 1), (node.i - 1, node.j + 1)]
        for coord in diagonal_neighbours_coords:
            if is_between(coord[0], 0, self.map.width - 1) and is_between(coord[1], 0, self.map.height - 1):
                diagonal_neighbours.append(self.map.nodes[coord[0]][coord[1]])
        return diagonal_neighbours
    
    #Algorithm only returns nodes which can be traversed to going in a direct diagonal path, ie. an AI can't travel
    #through the infinitesimally small corner of a node. This is to ensure the program is applicable for games like 'Tunnel Warrior'.
    def get_node_neighbours(self, node):
        neighbours = []
        adjacent_neighbours = self.get_adjacent_neighbours(node)
        diagonal_neighbours = self.get_diagonal_neighbours(node)
        for diag_node in diagonal_neighbours:
            neighbours_2 = self.get_adjacent_neighbours(diag_node)
            if num_identical(neighbours_2, adjacent_neighbours) == 2:
                neighbours.append(diag_node)
        neighbours += adjacent_neighbours
        return neighbours
    
    def set_costs(self, node):
        if not hasattr(node, 'previous'):
            node.g_cost = distance(node.get_pos(), self.map.player.get_pos())
        else: 
            node.g_cost = distance(node.previous.get_pos(), self.map.player.get_pos()) + distance(node.previous.get_pos(), node.get_pos()) * node.type
        node.h_cost = distance(node.get_pos(), self.map.destination.get_pos())
        node.f_cost = node.g_cost + node.h_cost
        
    def update_costs(self, node):
        g_cost = distance(node.previous.get_pos(), self.map.player.get_pos()) + distance(node.get_pos(), node.previous.get_pos())
        if g_cost < node.g_cost:
            node.g_cost = g_cost
            node.f_cost = node.g_cost + node.h_cost

class Game_Map:
    def __init__(self, width, height, node_size, node_border):
        self.width = width
        self.height = height
        self.node_size = node_size
        self.node_border = node_border
        self.nodes = [[Node(self, i, j) for j in range(height)] for i in range(width)]
        self.destination = Destination(self)
        self.player = Player(self)
        self.agent = Player(self)
        
        self.running = True
        self.generate_pygame()
        
    def generate_pygame(self):
        pg.init()
        pg.display.init()
        self.screen = pg.display.set_mode((self.width * self.node_size, self.height * self.node_size))
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                mx, my = pg.mouse.get_pos()
                x = mx//self.node_size
                y = my//self.node_size
                if pg.mouse.get_pressed()[0]:
                    self.nodes[x][y].set_type(0)
                elif pg.mouse.get_pressed()[1]:
                    self.nodes[x][y].set_type(2)
                elif pg.mouse.get_pressed()[2]:
                    self.nodes[x][y].set_type(1)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.destination.create(x * self.node_size, y * self.node_size)
                        if hasattr(self.player, 'xpos'):
                            self.refresh_colors()
                            Pathfinding(self)
                    elif event.key == pg.K_t:
                        self.player.create(x * self.node_size, y * self.node_size)
                        if hasattr(self.destination, 'xpos'):
                            self.refresh_colors()
                            Pathfinding(self)
                        
            self.draw()
            pg.display.update()
        
    def draw(self):
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes[i])):
                self.nodes[i][j].draw()
        self.destination.draw(self.screen)
        self.player.draw(self.screen)
        
    def refresh_colors(self):
        for nodes in self.nodes:
            for node in nodes:
                if node.type == 0: node.color = (0, 0, 0)
                elif node.type == 1: node.color = (255, 255, 255)
                elif node.type == 2: node.color = (0, 255, 0)
        
Game_Map = Game_Map(30, 20, 25, 1)

        