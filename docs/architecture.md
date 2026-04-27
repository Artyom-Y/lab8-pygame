# Architecture Documentation: Moving Squares (Pygame)

## Overview

This project is a small Pygame simulation where colored rectangles move around the screen, bounce on walls, change direction over time, and use simple threat/prey logic to chase smaller rectangles while fleeing larger ones. Rectangles also fade from blue to red over their lifespan and respawn when they expire.

## Core Modules

- `main.py` contains the complete runtime.
- `GameConfig` stores window, timing, and spawn constants.
- `MovingRect` extends `pygame.rect.Rect` with movement, color, and lifespan behavior.
- `init_window()` sets up Pygame, the display, sound, font, and global state.
- `update_screen()` runs the main loop, updates rectangles, and renders the frame.

## System Architecture

```mermaid
graph TB
    subgraph "Runtime Layer"
        MAIN["main()"]
        INIT["init_window()"]
        LOOP["update_screen()"]
    end

    subgraph "Game Objects"
        CFG["GameConfig"]
        RECT["MovingRect"]
    end

    subgraph "Support Functions"
        EVT["handle_events()"]
        SPAWN["create_moving_rects()"]
        BOUNCE["wall_bounce()"]
        FIND["find_threat_and_prey()"]
        STEER["run_and_chase_vect()"]
    end

    subgraph "Pygame Services"
        PG["pygame display, events, draw, font, mixer"]
    end

    MAIN --> INIT
    MAIN --> LOOP
    INIT --> PG
    LOOP --> EVT
    LOOP --> SPAWN
    LOOP --> BOUNCE
    LOOP --> FIND
    LOOP --> STEER
    LOOP --> RECT
    LOOP --> PG
    CFG -.-> RECT
    CFG -.-> INIT
    CFG -.-> LOOP
```

## Main Game Loop

```mermaid
sequenceDiagram
    participant App as "Application"
    participant Events as "Event Queue"
    participant Clock as "Pygame Clock"
    participant Rects as "MovingRect list"
    participant Draw as "Renderer"
    participant Sound as "Rebirth Sound"

    App->>App: init_window()
    App->>App: create_moving_rects(CONFIG.square_num)
    loop Each frame
        App->>Events: handle_events()
        App->>Clock: tick(CONFIG.fps)
        App->>Rects: iterate all rectangles
        App->>Rects: wall_bounce(rect, dt)
        App->>Rects: move_dir(dt)
        App->>Rects: randomize_dir(0.02)
        App->>Rects: randomize_speed(0.01)
        App->>Rects: find_threat_and_prey(rect, rects)
        App->>Rects: run_and_chase_vect(rect, threat, prey, 5)
        App->>Rects: decrease lifespan
        alt rectangle expired
            App->>Sound: play()
            App->>Rects: respawn new MovingRect
        else rectangle survives
            App->>Rects: keep rectangle alive
        end
        App->>Draw: render rectangles and UI text
        App->>Draw: pygame.display.flip()
    end
    App->>App: pygame.quit()
```

## Class Structure

```mermaid
classDiagram
    class "pygame.rect.Rect" {
        +x
        +y
        +width
        +height
        +centerx
        +centery
    }

    class "MovingRect" {
        +speed
        +vector
        +area
        +max_life
        +curr_life
        +color
        +set_speed() int
        +set_vector() pygame.Vector2
        +move_dir(dt) None
        +randomize_dir(chance) None
        +randomize_speed(chance) None
        +random_square() MovingRect
        +lerp_color(first, second, t) pygame.Color
    }

    class "GameConfig" {
        +width
        +height
        +fps
        +min_square_size
        +max_square_size
        +square_num
        +max_speed
    }

    "pygame.rect.Rect" <|-- "MovingRect"
```

## Control Flow

```mermaid
graph TD
    START["main()"] --> INIT["init_window()"]
    INIT --> LOOP["update_screen()"]
    LOOP --> EVENTS["handle_events()"]
    LOOP --> TICK["Clock tick()"]
    LOOP --> CREATE["create_moving_rects()"]
    LOOP --> FOR["for each rectangle"]
    FOR --> BOUNCE["wall_bounce()"]
    FOR --> MOVE["move_dir()"]
    FOR --> COLOR["lerp_color()"]
    FOR --> AI["find_threat_and_prey()"]
    AI --> STEER["run_and_chase_vect()"]
    FOR --> LIFE["decrease curr_life"]
    LIFE --> DEAD{"curr_life <= 0?"}
    DEAD -->|Yes| REBIRTH["play sound and respawn"]
    DEAD -->|No| KEEP["keep rectangle alive"]
    REBIRTH --> DRAW["draw frame and UI"]
    KEEP --> DRAW
    DRAW --> LOOP
```

## Data Flow

```mermaid
graph LR
    INPUT["Input state: rect positions, directions, lifespan"] --> PHYS["Physics: bounce and movement"]
    PHYS --> AI["AI: threat/prey selection and steering"]
    AI --> VIS["Visuals: color interpolation and drawing"]
    VIS --> AUDIO["Audio: respawn sound"]
    AUDIO --> NEXT["Next frame state"]
```

## Behavior Summary

- Movement uses `dt` from the clock, so position updates are frame-scaled.
- `pygame.Vector2` stores direction, while speed is a scalar value.
- Threat/prey logic compares rectangle area and distance to choose the closest larger and smaller rectangles.
- Color fades from `START_COLOR` to `END_COLOR` using linear interpolation.
- Expired rectangles are removed and replaced immediately to keep the object count stable.

## Performance Notes

| Area | Observation |
|---|---|
| Frame update | Linear over the current rectangle list for movement and drawing. |
| Threat search | Quadratic overall because each rectangle scans the full list for prey and threats. |
| Rendering | Simple draw calls with no batching or caching layer. |
| Best optimization path | Spatial partitioning would reduce the cost of proximity checks. |

## Limitations and Extensions

The current implementation is intentionally simple: it keeps runtime state in globals, does not model collisions between rectangles, and uses full-list scans for threat detection. The easiest next step is to move steering constants into `GameConfig`; the largest scaling improvement would be a spatial grid or quadtree for neighbor lookup.
