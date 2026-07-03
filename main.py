import pygame
import random
from board import Board, gen_empty_board
from themes import THEMES
from time import sleep
import sys, os

# needed for pyinstaller to work
def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

CELL_SIZE = 20
GRID_COLOR = (50, 50, 50)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 120

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
ICON = pygame.image.load(resource(f"./assets/icon{random.randint(1, 9)}.png"))
pygame.display.set_caption("The game of life... Now with colors!")
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()
FONT = pygame.font.Font("freesansbold.ttf", 15)

running = True
board = Board(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE)
dragging_left = False
dragging_right = False
sim_running = False
grid_width = 1
theme_index = 0
statusline = True
keybinds = True

dt = 0
interval_counter = 0
interval_ms = 125
#                   1/s   2/s  4/s  8/s  16/s  32/s   64/s
INTERVAL_PRESETS = [1000, 500, 250, 125, 62.5, 31.25, 15.625]


def write_statusline(board, sim_running):
    text = FONT.render(
        f"{'RUNNING' if sim_running else 'PAUSED'} | "
        f"Speed: {1000 / interval_ms:.0f} gens./sec. | "
        f"Generation: {board.generation} | Theme: {theme_index}",
        True,
        "white",
        THEMES[theme_index]["dead_color"],
    )
    text_rect = text.get_rect()
    text_rect.topleft = (0, 0)
    SCREEN.blit(text, text_rect)


def write_keybinds():
    text = FONT.render(
        "Left/Right Mouse - Set cell alive/dead \n"
        "Hold Shift+Left Mouse to set cell dead \n"
        "Space - Toggle simulation pause \n"
        "k - Toggle this message \n"
        "c - Clear board \n"
        "1-7 - Change speed \n"
        "g - Toggle grid \n"
        "t - Cycle theme \n"
        "n - Forward 1 generation \n"
        "s - Toggle statusline \n",
        True,
        "white",
        THEMES[theme_index]["dead_color"],
    )
    text_rect = text.get_rect()
    text_rect.bottomleft = (0, 600)
    SCREEN.blit(text, text_rect)


while running:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        shift_pressed = bool(pygame.key.get_mods() & pygame.KMOD_SHIFT)
        
        # ---------- Quit ----------
        if event.type == pygame.QUIT:
            running = False
        # ---------- Dragging ----------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if shift_pressed:
                    dragging_right = True
                else:
                    dragging_left = True
            elif event.button == 3:
                dragging_right = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_left = False
                dragging_right = False
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
            elif event.key in (
                pygame.K_1,
                pygame.K_2,
                pygame.K_3,
                pygame.K_4,
                pygame.K_5,
                pygame.K_6,
                pygame.K_7,
            ):
                interval_ms = INTERVAL_PRESETS[int(pygame.key.name(event.key)) - 1]
            # ---------- Grid Settings ----------
            elif event.key == pygame.K_g:
                grid_width = 0 if grid_width == 1 else 1
            # ---------- Color Settings ----------
            elif event.key == pygame.K_t:
                theme_index = (theme_index + 1) % len(THEMES)
            # ---------- Simulate 1 Generation ----------
            elif event.key == pygame.K_n:
                board.simulate()
            # ---------- Statusline Toggle ----------
            elif event.key == pygame.K_s:
                statusline = not statusline
            # ---------- Keybinds List Toggle ----------
            elif event.key == pygame.K_k:
                keybinds = not keybinds

    if dragging_left:
        board.click(mx, my)
    elif dragging_right:
        board.click(mx, my, False)

    if sim_running and interval_counter >= interval_ms:
        board.simulate()
        interval_counter = 0

    theme_colors = THEMES[theme_index]
    board.draw(SCREEN, border_width=grid_width, **theme_colors)

    if statusline:
        write_statusline(board, sim_running)

    if keybinds:
        write_keybinds()

    pygame.display.flip()
    dt = clock.tick(FPS)
    interval_counter += dt

pygame.quit()
