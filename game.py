import pygame
from random import randint
class sand:
    def __init__(self):
        self.has_moved = False
        diff=randint(-20,20)
        r = 194 + diff
        g = 178 + diff 
        b = 128 + diff
        self.color = (r,g,b)
    
    def move(self, grid, old_y, old_x, new_y, new_x):
        grid[new_y][new_x], grid[old_y][old_x] = grid[old_y][old_x], grid[new_y][new_x]

    def check_bottom_left(self, x,y, grid, other):
        # Left edge check
        if x <= 0:
            if other == True:
                return False
            else:
                return self.check_bottom_right(x,y, grid, True)
        # Regular checks
        if isinstance(grid[y+1][x-1], (empty, water)):
            self.move(grid, y, x, y+1, x-1)
            return True
        else:
            if other == True:
                return False
            else:
                return self.check_bottom_right(x,y, grid, True)

    def check_bottom_right(self, x,y, grid, other):
        # Right edge check
        if x >= width - 1:
            if other == True:
                return False
            else:
                return self.check_bottom_left(x,y, grid, True)
        # Regular checks
        if isinstance(grid[y+1][x+1], (empty, water)):
            self.move(grid, y, x, y+1, x+1)
            return True
        else:
            if other == True:
                return False
            else:
                return self.check_bottom_left(x,y, grid, True)

    def check_below(self, x,y, grid):
        # Floor check
        if y >= height - 1:
            return False
        # Regular checks
        if isinstance(grid[y+1][x], (empty, water)):
            self.move(grid, y, x, y+1, x)
            return True
        else:
            if randint(0,1) == 0:
                return self.check_bottom_left(x,y, grid, False)
            else:
                return self.check_bottom_right(x,y, grid, False)

class empty:
    def __init__(self):
        self.color = (0,0,0)

class water:
    def __init__(self):
        diff=randint(-20,20)
        r = 64 + diff
        g = 164 + diff 
        b = 223 + diff
        self.color = (r,g,b)

width, height=50,50
grid = [[empty() for _ in range(width)] for _ in range(height)]
for y in range(10, 20):
    for x in range(10,20):
        grid[y][x] = sand()
# for y in range(9,15):
#     grid[y][24] = sand()
cell_size=10

pygame.init()
screen = pygame.display.set_mode((width * cell_size, height * cell_size))
clock = pygame.time.Clock()
running = True

def draw_grid():
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            pygame.draw.rect(
                screen,
                cell.color,
                (x * cell_size, y * cell_size, cell_size, cell_size)
            )
    pygame.display.flip()



def update():
    for y in range(height-1, -1, -1):  # Bottom to top
        for x in range(width):
            cell = grid[y][x]
            if isinstance(cell, sand) and not cell.has_moved:
                if cell.check_below(x, y, grid):
                    cell.has_moved = True
    
    # Reset has_moved flag for next frame
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            if isinstance(cell, sand):
                cell.has_moved = False

    pygame.time.delay(50)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    update()
    draw_grid()
    