import pygame
BLACK = (0,0,0)    # Obstacle
RED = (255,0,0)    # invalid/closed node
BLUE = (0,0,255)   # destination
GREEN = (0,255,0)  # valid node
WHITE = (255,255,255) # empty node
TEAL = (8,232,222)    # path
ORANGE = (255, 102,0) # start

class Node:
    
    def __init__(self, row, col, side, total_rows):
        self.row = row
        self.col = col
        self.x = row * side     # pixels
        self.y = col * side
        self.color = WHITE
        self.side = side
        self.total_rows = total_rows

    def get_position(self):
        return (self.row, self.col)

    # if color is red, then it is a closed node
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN
    
    def is_obstacle(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_destination(self):
        return self.color == BLUE
    
    def reset(self):
        self.color = WHITE           # check this!!! 30 min
    
    def close(self):
        self.color = RED

    def open(self):
        self.color = GREEN

    def start(self):
        self.color = ORANGE
    
    def obstacle(self):
        self.color = BLACK
    
    def destination(self):
        self.color = BLUE
    
    def path(self):
        self.color = TEAL
    
    def display(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.side, self.side)) # (x,y,side,side)

    def update_neighbors(self, grid):
        self.neighbors = []

        # check below
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col])
        
        # check above
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        # check right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])
        
        # check left
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])

    
    # less than 
    def __lt__(self, other):
        return False

