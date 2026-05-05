# Python to Vanilla JS Port Plan

## Goal
Port the current `main.py` pygame application into a single standalone `index.html` file under `web/`, using only HTML, CSS, Vanilla JavaScript, and HTML5 Canvas.

This plan keeps the current behavior and structure as close as possible to the Python version. It does not implement the port yet.

## Non-Negotiable Constraints

- Preserve the current data flow from `main.py`.
- Keep every Python class as a JavaScript class.
- Keep function and variable names identical where possible, translating to camelCase only when JS style makes that necessary.
- Do not refactor logic, fix bugs, or improve behavior while porting.
- Map Python lists to JS arrays and Python dictionaries to JS objects.
- Replace the pygame loop with `requestAnimationFrame()`.
- Use `CanvasRenderingContext2D` for all rendering.
- Keep the final deliverable self-contained in one `index.html` file.
- Add short JSDoc-style comments near the main classes or loop to explain the pygame equivalent.

## Source Inventory From `main.py`

The port should preserve the same conceptual units:

- `GameConfig` dataclass becomes a JS class with the same fields.
- `MovingRect` remains a class and keeps the same responsibilities: speed, vector, movement, collisions, trail tracking, color interpolation, and respawn helpers.
- Global state stays global in the script: `CONFIG`, `SCREEN`, `CLOCK`, `IS_OPEN`, `FONT`, `REBIRTH_SOUND`, `START_COLOR`, `END_COLOR`, `LINE_COLOR`.
- Helper functions stay as separate functions:
  - `init_window()`
  - `handle_events()`
  - `create_moving_rects()`
  - `wall_bounce()`
  - `wall_warp()`
  - `find_threat_and_prey()`
  - `run_and_chase_vect()`
  - `update_screen()`
  - `main()`

## Planned JS Class Mapping

1. `GameConfig`
   - Store width, height, fps, size limits, counts, chances, lifespan, and trail length.
   - Instantiate one shared `CONFIG` object from it, matching the Python singleton-style usage.

2. `Vector2`
   - Represent `x` and `y` and provide the small set of operations used by the Python code: length, lengthSquared, normalize, rotate, add, and scalar multiply.
   - This keeps the movement and chase math visually close to the Python version.

3. `Rect`
   - Provide a minimal rectangle base class to mirror the `pygame.Rect` behavior relied on by `MovingRect`.
   - Include position, size, center access, and collision checks.

4. `MovingRect extends Rect`
   - Keep the same fields: `speed`, `vector`, `area`, `max_life`, `curr_life`, `color`, `last_positions`.
   - Keep the same methods: `set_speed()`, `set_vector()`, `move_dir()`, `randomize_dir()`, `randomize_speed()`, `check_collision()`, `draw_trail()`, `random_square()`, `lerp_color()`.

5. `Color`
   - Use a small class or structured object for RGBA values so color interpolation stays explicit and readable.

## Runtime Loop Plan

The Python code uses `CLOCK.tick(CONFIG.fps)` and then applies that delta to movement and lifespan math. The JS version should mirror that timing model as closely as possible.

Plan:

- Use `requestAnimationFrame(loop)` as the main driver.
- Store the previous timestamp from the last animation frame.
- Compute `dt` in milliseconds from the difference between the current timestamp and the previous one.
- Pass that `dt` through the same movement and life calculations used now.
- Keep the target frame rate concept through `CONFIG.fps`, but do not change the simulation rules.
- Stop the loop when `IS_OPEN` becomes false.

## Rendering Plan

Replace pygame drawing calls with canvas calls while keeping the same draw order.

- `SCREEN.fill(...)` becomes `ctx.fillStyle = ...; ctx.fillRect(...)`.
- `pygame.draw.rect(...)` becomes `ctx.fillRect(...)`.
- `pygame.draw.line(...)` becomes `ctx.beginPath()`, `ctx.moveTo()`, `ctx.lineTo()`, `ctx.stroke()`.
- `SCREEN.blit(...)` for the FPS text becomes `ctx.fillText(...)`.
- `pygame.display.flip()` becomes the natural canvas redraw at the end of the animation frame.

The canvas setup should include:

- A minimal CSS block to center the canvas.
- A dark background that matches the current pygame clear color.
- One `<canvas>` element sized to `CONFIG.width` and `CONFIG.height`.

## Input And Events

The current Python app only reacts to quitting the window. The JS port should map that behavior, not add extra gameplay input.

- Use `window.addEventListener('beforeunload', ...)` or `pagehide` to mirror shutdown.
- Use `document.addEventListener('visibilitychange', ...)` only if needed to keep the loop state consistent.
- If future mouse or keyboard controls are added, map them with standard `addEventListener` calls and keep them isolated from the simulation logic.

## Audio Plan

Replace `pygame.mixer.Sound("media/pop.mp3")` with browser audio support.

- Preload an `Audio` object for `media/pop.mp3`.
- Preserve the volume setting at `0.5`.
- Trigger the sound at the same respawn moment currently handled by `REBIRTH_SOUND.play()`.

## Logic Preservation Notes

The port should preserve the current simulation rules exactly:

- `create_moving_rects()` should keep the same parameter handling, including the keyed counts map.
- `wall_bounce()` should keep the same border logic and direction inversion.
- `wall_warp()` should remain available even if it is currently marked buggy in the Python file.
- `find_threat_and_prey()` should still scan all rectangles and pick the nearest larger and smaller targets.
- `run_and_chase_vect()` should preserve the same vector blending logic and danger weighting.
- Eating, growth, lifespan decay, and respawn should remain in the same order as the Python loop.

## File Structure For The Final Port

The final implementation should live in one file:

- `web/index.html`

The file should contain:

- Minimal CSS.
- The canvas element.
- A single `<script>` block with the ported logic.
- Brief comments that point out the pygame equivalent of the main classes and the animation loop.

## Implementation Order

1. Create the HTML shell and canvas.
2. Implement the lightweight support classes needed to preserve the Python structure.
3. Port the globals and configuration values.
4. Port the helper functions one by one without changing logic.
5. Replace the main loop with `requestAnimationFrame()` and delta-time handling.
6. Port rendering, HUD text, and audio.
7. Add the short JSDoc comments for the main classes and the loop.
8. Verify the resulting file is still a single standalone document.

## Explicit Stop Point

Do not implement the port yet. This document is the planning artifact only and should be used as the guide for the later `index.html` conversion.