# Moving Squares (Pygame)

Small starter project for a pygame app where multiple squares move around the window with randomized directions.

This is an early version and the project will evolve over time. The current goal is to keep a simple, readable foundation that is easy to extend.

## Overview

- Creates an `800x800` pygame window.
- Spawns multiple square objects near the center of the screen.
- Moves each square every frame using direction values (`dir_x`, `dir_y`).
- Randomizes movement direction periodically.
- Runs at a fixed FPS loop and handles window-close events.

Core implementation lives in `main.py` and uses:

- `GameConfig` for window and game constants.
- `MovingRect` (subclass of `pygame.Rect`) for per-square movement logic.
- A classic update/render game loop.

## Setup

### 1. Create and activate a virtual environment

Windows (PowerShell):

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

If `requirements.txt` is not populated yet, install pygame directly:

```powershell
pip install pygame
```

## Usage

Run the app from the project root:

```powershell
python main.py
```

What you should see:

- A dark background window.
- Blue squares moving continuously.
- Motion directions changing every short interval.

Close the window to stop the app.

## Next Iterations (Planned)

- Add edge/boundary behavior (bounce or wrap).
- Add keyboard input for interaction.
- Add score/state display and cleaner game structure.
- Add tests for non-visual logic where practical.
