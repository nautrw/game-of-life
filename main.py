import pygame

BLOCK_SIZE = 20
GRID_COLOR = (50, 50, 50)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True

def draw_grid():
    for i in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        pygame.draw.line(SCREEN, GRID_COLOR, (i, 0), (i, WINDOW_HEIGHT))
        pygame.draw.line(SCREEN, GRID_COLOR, (0, i), (WINDOW_WIDTH, i))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    SCREEN.fill("black")
    draw_grid()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()