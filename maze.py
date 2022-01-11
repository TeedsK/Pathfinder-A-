from refresh import Refresh_Drawn
import pygame
from queue import PriorityQueue

#The dimensions of the game 
#
# Width is the size of the screen
#
# Rows are the amount of rows seen in the game 
WIDTH = 800
ROWS = 100

# Whether or not the path is allowed to go diagonally
# True = yes - diagonal lines are ALLOWED
# False = no - diagonal lines are NOT allowed
DIAGONAL = False

#Creates the pygame
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* pathfinding")


# The color options used in the program
# Change the right hand side values to change the colors
SEARCHED = (227, 227, 227)
START = (77, 212, 136)
END = (212, 77, 77)
NEIGHBORS = (247, 211, 50)
EMPTY = (255,255,255)
GRAY = (150,150,150)
WALL = (0,0,0)
BEST_PATH = (153, 89, 236)
TO_SEARCH = (202, 202, 202)

#Initaites the refresh rate object to re-draw the screen at a given rate
REFRESH = Refresh_Drawn(15)

#The node class
class Node:

    #Initaites the node object
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = EMPTY
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Returns the position of the node
    def get_pos(self):
        return self.row, self.col

    #Sets the color of the node to be the best path color
    def set_as_path(self):
        self.color = BEST_PATH
    
    #Sets hte color of the node to be the start
    def set_as_start(self):
        self.color = START

    #Sets hte color of the node to be the end
    def set_as_end(self):
        self.color = END

    #Sets the color of the node to be a wall
    def set_as_wall(self):
        self.color = WALL

    def get_wall(self):
        return self.color == WALL

    #Sets the color of the node to be empty
    def set_as_empty(self):
        self.color = EMPTY

    #Sets the color of the node to be empty
    def set_as_searched(self):
        self.color = SEARCHED

    def set_as_to_search(self):
        self.color = TO_SEARCH

    def reset(self):
        self.color = EMPTY

    #Draws the node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    #Updates the nodes nearby
    def update_neighbors(self, grid):
        self.neighbors = []

        #Node Below
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].get_wall(): 
            self.neighbors.append(grid[self.row + 1][self.col])

        #Node Above
        if self.row > 0 and not grid[self.row - 1][self.col].get_wall(): 
            self.neighbors.append(grid[self.row - 1][self.col])

        #Node Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].get_wall(): 
            self.neighbors.append(grid[self.row][self.col + 1])

        #Node Left
        if self.col > 0 and not grid[self.row][self.col - 1].get_wall(): 
            self.neighbors.append(grid[self.row][self.col - 1])

        #Checks if going diagonal is allowed
        if DIAGONAL:
            #Node Top Left (Dyaginal)
            if (self.row > 0 and self.col > 0) and not grid[self.row - 1][self.col - 1].get_wall(): 
                self.neighbors.append(grid[self.row - 1][self.col - 1])

            #Node Top Right 
            if (self.row > 0 and self.col < self.total_rows - 1) and not grid[self.row - 1][self.col + 1].get_wall(): 
                self.neighbors.append(grid[self.row - 1][self.col + 1])

            #Node Bottom Left
            if (self.col > 0 and self.row < self.total_rows - 1) and not grid[self.row + 1][self.col - 1].get_wall(): 
                self.neighbors.append(grid[self.row + 1][self.col - 1])

            #Node Bottom Right
            if (self.col < self.total_rows - 1 and self.row < self.total_rows - 1) and not grid[self.row + 1][self.col + 1].get_wall(): 
                self.neighbors.append(grid[self.row + 1][self.col + 1])


    def __lt__(self, other):
        return False

#calculates distance by using manhatan distance
def calculate_h_value(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x1 - x2) + abs(y1 - y2)

#Creates the best path 
def generate_best_path(parents, current, draw):
    # refresh = Refresh_Drawn(ROWS / 10)
    
    count = 0
    divisor = ROWS / 10
    while current in parents:
        current = parents[current]
        current.set_as_path()
        REFRESH.refresh()
        
        # if count % divisor == 0:
        #     draw()
        # count += 1

#Resets the board
def reset_simulation():
    pass


#the start algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    parent = {}
    g_score = {Node: float("inf") for row in grid for Node in row}
    g_score[start] = 0
    f_score = {Node: float("inf") for row in grid for Node in row}
    f_score[start] = calculate_h_value(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        #to stop
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        #makes the path
        if current == end:
            generate_best_path(parent, end, draw)
            end.set_as_end()
            start.set_as_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
    
            #checks if better path
            if temp_g_score < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + calculate_h_value(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_as_to_search()
                    
        REFRESH.refresh()
        
        if current != start:
            current.set_as_searched()

    return False

def generate_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for x in range(rows):
        pygame.draw.line(win, GRAY, (0, x * gap), (width, x * gap))
        for y in range(rows):
            pygame.draw.line(win, GRAY, (y * gap, 0), (y * gap, width))

def draw(win, grid, rows, width):
    win.fill(EMPTY)
    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_position(position, rows, width):
    gap = width // rows
    y,x = position

    row = y // gap
    col = x // gap

    return row, col

def main(win, width):
    
    grid = generate_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue
        
            #Left mouse button
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = get_clicked_position(position, ROWS, width)
                node = grid[row][col]
                print(node == start)
                print(node == end)
                print(end)
                print("--------")
                if not start and node != end:
                    start = node
                    node.set_as_start()

                elif not end and node != start:
                    end = node
                    end.set_as_end()
                
                elif not node == start and not node == end:
                    node.set_as_wall()
            #Right mouse button
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = get_clicked_position(position, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    REFRESH.set_draw_function(lambda: draw(win, grid, ROWS, width))
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
    
    pygame.quit()


main(WIN, WIDTH)