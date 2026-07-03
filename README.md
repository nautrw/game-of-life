# Game of Life
Conway's Game of Life implemented in Pygame with many features including themes, simulation flow control, and speed adjustment.

https://github.com/user-attachments/assets/b3728412-8ebf-4f69-9278-de5dc4ba8b8c

# Features
- Many keyboard shortcuts to control the simulation (pause, play, forward one generation, etc.).
- Many color themes and customizability options.
- Easily draw or erase patterns with the mouse.
- Messages show important information and keybinds.

# Installation
## Releases (Recommended)
Head over to [the releases page](https://github.com/nautrw/game-of-life/releases/latest) and download the file for your operating system:
- Windows: `GameOfLife_Windows.exe` (A Windows defender warning might pop up)
- Linux: `GameOfLife_Linux`

Simply execute the file and it should launch.

## Build from scratch:
**Minimum Python version: 3.6**

1. Clone the GitHub repository onto your system.
2. Open a shell inside the folder of the cloned repository.
3. Copy and run the following command:
- On Windows (Powershell):
```powershell
python -m venv .venv; .venv\scripts\activate; python -m pip install -r requirements.txt; pyinstaller --onefile --windowed --add-data "assets/*;assets" --icon=assets/desktop_icon.ico --exclude-module numpy --exclude-module pandas --exclude-module scipy --exclude-module matplotlib --name="GameOfLife" main.py
```
- On Linux:
```sh
python -m venv .venv && .venv/scripts/activate && python -m pip install -r requirements.txt && pyinstaller --onefile --windowed --add-data "assets/*:assets" --icon=assets/desktop_icon.ico --exclude-module numpy --exclude-module pandas --exclude-module scipy --exclude-module matplotlib --name="GameOfLife" main.py
```
4. The executable should be in the `./dist/` folder:
- On Linux: `./dist/GameOfLife`
- On Windows: `.\dist\GameOfLife.exe`

# How It Works
This project is an implementation of Conway's Game of Life. There is a square grid of cells, which are either alive or dead.

Between generations, the following rules are executed:

1. A live cell with less than 2 neighbors dies by underpopulation.
2. A live cell with more than 3 neighbors dies by overpopulation.
3. A live cell with 2 or 3 neighbors lives on.
4. A dead cell with 3 live neighbors becomes a live cell by reproduction.

In the code, this grid is represented as a 2-dimensional array, with each individual cell being a boolean (True if alive, False if dead). This allows for something similar to a coordinate system for the grid.

Users are able to draw onto the grid to create patterns, and then let the simulation decide if cells live or die based on the rules.

Live neighbors are counted using a function that checks every neighboring cell and adds 1 to a count if it is alive.

Games made in Pygame usually have a main while loop in which graphics are displayed, user input is checked, etc. To make anything toggleable, I used variables and ran whatever code if they were set to `True` inside the main while loop. Keybinds simply toggle the variable.

To draw the grid, rectangles are drawn for every cell. To allow for clicking on a cell to make it alive, I get the position of the mouse when the click occurs, and then calculate what cell that would correspond to using the dimensions of the window, and the size and amount of the cells. Themes and speed presets are cycleable by using an array to store them, and then another variable storing the index.

# Libraries Used
- `pygame-ce` - Graphics, user input, etc. The main library of the project.
- `pyinstaller` - Compiling the project.