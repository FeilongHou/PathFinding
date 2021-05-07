import pygame
import math
from queue import PriorityQueue
from Node import Node

WIN_SIZE = 800
WINDOW = pygame.display.set_mode((WIN_SIZE,WIN_SIZE))

pygame.display.set_caption("A* Path Finding")        # setting title for the window

# h(x) distance we use Manhattan distance
# since we dont want a diagonal path
def h(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows, size):
    grid = []
    side = size // rows
    # this is row
    for i in range(rows):
        grid.append([])
        # this is column since we have a square gird
        for j in range(rows):
            node = Node(i, j, side, rows)
            grid[i].append(node)

    return grid

def draw_grid(window, rows, size):
    side = size // rows
    GREY = (100,100,100)
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * side), (size, i * side))   # starting position and ending position
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * side, 0), (j * side, size))

def display(window, grid, rows, size):
    # fill color on the window
    window.fill((255,255,255))

    for row in grid:
        for node in row:
            node.display(window)

    draw_grid(window, rows, size)
    pygame.display.update()

def clicked_node(position, rows, size):
    side = size // rows
    y,x = position   # pixel value

    # these are the the coordinate of the node 
    # if we have a 10x10 grid, the (row, col) = (5th, 5th)
    row = y // side
    col = x // side
    return row, col

def display_path(came_from, current_node, display):
    while current_node in came_from:
        # track back to start
        # current destination = {destination : destination - 1}
        current_node = came_from[current_node]
        current_node.path()
        display()


def A_star(display, grid, start_node, destination_node):
    # keep track of iteration to decide which one to use when having the same distance
    iteration = 0
    # PriorityQueue will get the min f score node
    open_set = PriorityQueue()
    # (f, iteration, node)
    open_set.put((0, iteration, start_node))
    came_from = {}

    # set all node to have infinity distance from start except start
    g = {node: float("inf") for row in grid for node in row}
    g[start_node] = 0

    # set all node to have infinity distance from destination except destination
    f = {node: float("inf") for row in grid for node in row}
    f[start_node] = h(start_node.get_position(), destination_node.get_position()) 

    open_set_hash = {start_node}

    while not open_set.empty():
        # quit game is bugged
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # getting the node
        current_node = open_set.get()[2]
        open_set_hash.remove(current_node)

        if current_node == destination_node:
            display_path(came_from, destination_node, display)
            # redraw the destination blue 
            destination_node.destination()
            start_node.start()
            return True
        
        for neighbor in current_node.neighbors:
            tem_g_score = g[current_node] + 1

            # if we find a better path
            if tem_g_score < g[neighbor]:
                # came from has {n+1 : n}
                came_from[neighbor] = current_node
                g[neighbor] = tem_g_score
                f[neighbor] = tem_g_score + h(neighbor.get_position(), destination_node.get_position())
                if neighbor not in open_set_hash:
                    iteration += 1
                    open_set.put((f[neighbor], iteration, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.open()
        
        display()
        # just checked current_node, make is close
        if current_node != start_node:
            current_node.close()
        
    return False


def main(window, size):
    ROWS = 50
    grid = make_grid(ROWS, size)

    start_node = None
    destination_node = None
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # if we press the left mouse button
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = clicked_node(position, ROWS, size)
                node = grid[row][col]

                # first click is the starting node
                if not start_node and node != destination_node and node.color == (255,255,255):
                    start_node = node
                    start_node.start()
                # second click is the destination node and not allow overwriting each other
                elif not destination_node and node != start_node and node.color == (255,255,255):
                    destination_node = node
                    destination_node.destination()
                
                elif node != start_node and node != destination_node:
                    obstacle = node
                    obstacle.obstacle()
                
            
            # if we press the right mouse button we reset
            if pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = clicked_node(position, ROWS, size)
                node = grid[row][col]
                node.reset()
                if node == start_node:
                    start_node = None
                elif node == destination_node:
                    destination_node = None

            # if press space we run the algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start_node and destination_node:
                    # update all neighbors for all node
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    A_star(lambda: display(window, grid, ROWS, size), grid, start_node, destination_node)

            # if press r, reset game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start_node = None
                    destination_node = None
                    grid = make_grid(ROWS, WIN_SIZE)

        display(window, grid, ROWS, size)

main(WINDOW, WIN_SIZE)