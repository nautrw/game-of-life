import pygame
from board import Board, gen_empty_board
from themes import THEMES

CELL_SIZE = 20
GRID_COLOR = (50, 50, 50)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 610

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("The game of life... Now with colors!")
clock = pygame.time.Clock()
FPS = 8
SPEED_PRESETS = [1, 2, 4, 8, 16, 32, 64, 128, 256]
FONT = pygame.font.Font('freesansbold.ttf', 10)

running = True
board = Board(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
dragging_left = False
dragging_right = False
sim_running = False
grid_width = 1
theme_index = 0

def write_statusline(board, sim_running):
    text = FONT.render(
        f"{'RUNNING' if sim_running else 'PAUSED'} | FPS: {FPS} |"
        f"Generation: {board.generation}", True, 'white')
    text_rect = text.get_rect()
    text_rect.topleft = (0, 600)
    SCREEN.blit(text, text_rect)

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
                board.generation = 0
            # ---------- Speed Settings ----------   
            elif event.key == pygame.K_EQUALS:
                FPS += 1
            elif event.key == pygame.K_MINUS:
                FPS -= 1 if FPS > 1 else 0
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                             pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, 
                             pygame.K_9):
                FPS = SPEED_PRESETS[int(pygame.key.name(event.key)) - 1]
            # ---------- Grid Settings ----------   
            elif event.key == pygame.K_g:
                grid_width = 0 if grid_width == 1 else 1
            # ---------- Color Settings ----------   
            elif event.key == pygame.K_t:
                if theme_index == len(THEMES) - 1:
                    theme_index = 0
                else:
                    theme_index += 1
            # ---------- Simulate 1 Generation ----------   
            elif event.key == pygame.K_n:
                board.simulate()
             
        if dragging_left:
            board.click(mx, my)
        elif dragging_right:
            board.click(mx, my, False)
    
    if sim_running:
        board.simulate()

    theme_colors = THEMES[theme_index]
    board.draw(SCREEN, border_width=grid_width, **theme_colors)
    write_statusline(board, sim_running)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
