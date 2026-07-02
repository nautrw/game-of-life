import pygame
from board import Board, gen_empty_board

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
