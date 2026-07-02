import time
import pygame

CELL_SIZE = 20
GRID_COLOR = (50, 50, 50)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True

def count_live_neighbors(grid, row, column):
    rows, columns = len(grid), len(grid[0])
    neighbors = []
    
    # fmt: off 
    directions = [
        (-1, -1), (-1, 0), (-1, 1), # Top-left, Top, Top-right
        (0, -1),          (0, 1),   # Left, Right
        (1, -1), (1, 0), (1, 1)     # Bottom-left, Bottom, Bottom-right
    ]
    # fmt: on

    for dr, dc in directions:
        new_row, new_col = row + dr, column + dc

        if 0 <= new_row < rows and 0 <= new_col < columns:
            neighbors.append(grid[new_col][new_row])
    
    return neighbors.count(True)

class Board:
    def __init__(self, width, height, cell_size):
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.cell_size = cell_size
        # This way, the cell grids work more like pygame coordinates where
        # +x moves right but +y moves down
        self.cells = [[False for _ in range(self.rows)] for _ in range(self.columns)]
        self.cells[1][0] = True
        self.cells[1][1] = True
        self.cells[1][2] = True

    def draw(
        self,
        screen,
        border_width=1,
        dead_color="black",
        alive_color="white",
        border_color="gray20",
    ):
        screen.fill(border_color)

        for column in range(self.columns):
            for row in range(self.rows):
                cell = self.cells[column][row]
                color = dead_color if not cell else alive_color
                cx = column * self.cell_size
                cy = row * self.cell_size
                width = self.cell_size - border_width

                pygame.draw.rect(screen, color, (cx, cy, width, width))

    def click(self, x, y, new_state=True):
        # fixes this bug where the user can move the mouse out of the window
        # to the right and it keeps drawing but wrapped around
        if x < 0 or y < 0:
            return
        
        row = x // self.cell_size
        column = y // self.cell_size

        try:
            self.cells[row][column] = new_state
        except IndexError:
            pass
    
    def simulate(self):
        neighbor_offsets = [(-1, -1), (0, -1), (1, -1), (-1,  0), (1,  0), (-1,  1), (0,  1), (1,  1)]   
        
        for column in range(self.columns):
            for row in range(self.rows):
                live_neighbors = 0
                for offset in neighbor_offsets:
                    new_row = (row + offset[0]) % self.rows
                    new_column = (column + offset[1]) % self.columns

                    try:
                        if self.cells[new_row][new_column]:
                            live_neighbors += 1
                    except IndexError:
                        pass
                
                if live_neighbors < 2:
                    self.cells[column][row] = False # death by underpopulation
                elif 2 > live_neighbors > 3:
                    pass # cell lives on
                elif live_neighbors > 3:
                    self.cells[column][row] = False # death by overpopulation
                elif not self.cells[column][row] and live_neighbors == 3:
                    self.cells[column][row] = True # reproduction


board = Board(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
dragging_left = False
dragging_right = False

while running:
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging_left = True
            elif event.button == 3:
                dragging_right = True 
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_left = False
            elif event.button == 3:
                dragging_right = False
        
        if dragging_left:
            board.click(mx, my)
        elif dragging_right:
            board.click(mx, my, False)

    board.simulate()
    board.draw(SCREEN, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
