# Moving Squares (Pygame)

Small starter project for a pygame app where multiple squares move around the window with randomized directions.

This is an early version and the project will evolve over time. The current goal is to keep a simple, readable foundation that is easy to extend.

## Overview

- Creates a pygame window.
- Spawns multiple square objects.
- Moves each square every frame using direction vector mulitplied by speed vector.
- Randomizes movement direction periodically.
- Runs at a fixed FPS loop and handles window-close events.
- Misc features like wall bouncing, smaller rectangles running away from bigger ones, lifespan

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

## Usage

Run the app from the project root:

```powershell
python main.py
```

Close the window to stop the app.
