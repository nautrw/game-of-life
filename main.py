import pygame

CELL_SIZE = 20
GRID_COLOR = (50, 50, 50)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True


class Board:
    def __init__(self, width, height, cell_size):
        self.rows = height // cell_size
        self.columns = width // cell_size
        self.cell_size = cell_size
        # This way, the cell grids work more like pygame coordinates where
        # +x moves right but +y moves down
        self.cells = [[False for _ in range(self.rows)] for _ in range(self.columns)]

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

    def click(self, x, y):
        row = x // self.cell_size
        column = y // self.cell_size

        self.cells[row][column] = not self.cells[row][column]


board = Board(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
dragging = False

while running:
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        
        if dragging:
            board.click(mx, my)

    board.draw(SCREEN, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
