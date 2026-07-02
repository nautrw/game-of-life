import pygame

def count_live_neighbors(grid, column, row):
    columns, rows = len(grid), len(grid[0])
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

def gen_empty_board(columns, rows):
        # This way, the cell grids work more like pygame coordinates where
        # +x moves right but +y moves down
    return [[False for _ in range(rows)] for _ in range(columns)]

class Board:
    def __init__(self, width, height, cell_size):
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.cell_size = cell_size
        self.generation = 0
        self.cells = gen_empty_board(self.columns, self.rows)

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
        
        column = y // self.cell_size
        row = x // self.cell_size

        try:
            self.cells[row][column] = new_state
        except IndexError:
            pass
    
    def simulate(self):
        temp_board = [column.copy() for column in self.cells]
        
        for column in range(self.columns):
            for row in range(self.rows):
                live_neighbors = count_live_neighbors(self.cells, column, row)
                alive = self.cells[column][row]
                
                if alive:
                    # death by underpopulation or overpopulation
                    if live_neighbors < 2 or live_neighbors > 3:
                        temp_board[column][row] = False
                    else:
                        pass # cell lives on
                else:
                    if live_neighbors == 3:
                        temp_board[column][row] = True # cell reproduces
        
        self.cells = temp_board
        self.generation += 1
    
    def clear(self):
        self.cells = gen_empty_board(self.columns, self.rows)