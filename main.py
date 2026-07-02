import pygame

CELL_SIZE = 20
GRID_COLOR = (50, 50, 50)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
FPS = 12
running = True
SPEED_PRESETS = [1, 2, 4, 8, 16, 32, 64, 128, 256]

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
        
        row = x // self.cell_size
        column = y // self.cell_size

        try:
            self.cells[row][column] = new_state
        except IndexError:
            pass
    
    def simulate(self):
        temp_board = [column.copy() for column in self.cells]
        
        for column in range(self.columns):
            for row in range(self.rows):
                live_neighbors = count_live_neighbors(self.cells, column, row)
                
                if self.cells[column][row]:
                    # death by underpopulation or overpopulation
                    if live_neighbors < 2 or live_neighbors > 3:
                        temp_board[column][row] = False
                    else:
                        pass # cell lives on
                else:
                    if live_neighbors == 3:
                        temp_board[column][row] = True # cell reproduces
        
        self.cells = temp_board
    
    def clear(self):
        self.cells = gen_empty_board(self.columns, self.rows)

board = Board(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
dragging_left = False
dragging_right = False
sim_running = False

while running:
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        # ---------- Quit ----------   
        if event.type == pygame.QUIT:
            running = False
        # ---------- Dragging ----------   
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
        elif event.type == pygame.KEYDOWN:
            # ---------- Pausing ----------   
            if event.key == pygame.K_SPACE:
                sim_running = not sim_running
            # ---------- Clear Board ----------   
            elif event.key == pygame.K_c:
                board.clear()
            # ---------- Speed Settings ----------   
            elif event.key == pygame.K_EQUALS:
                FPS += 1
            elif event.key == pygame.K_MINUS:
                FPS -= 1 if FPS > 1 else 0
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                             pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, 
                             pygame.K_9):
                FPS = SPEED_PRESETS[int(pygame.key.name(event.key)) - 1]

        
        if dragging_left:
            board.click(mx, my)
        elif dragging_right:
            board.click(mx, my, False)

    if sim_running:
        board.simulate()
    else:
        pass
    board.draw(SCREEN)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
