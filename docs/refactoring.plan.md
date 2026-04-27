# Overview

`main.py` is a compact Pygame project that already works, but it mixes setup, game logic, movement, AI behavior, drawing, and global state in one file. The code is understandable, but several parts are harder to follow than they need to be for a first-year student: there are many global variables, a few magic numbers, some repeated logic, and a few functions that do more than one job.

The goal of this refactoring is not to redesign the project. The goal is to keep the same behavior while making the code easier to read, easier to explain, and easier to change in small steps.

# Refactoring Goals

- Make the game loop easier to read.
- Reduce the number of magic numbers.
- Make names and responsibilities clearer.
- Group related logic into small helper functions.
- Keep the current gameplay behavior the same.
- Add concise inline comments in the final code that explain what changed, why it helps, and the programming concept involved.

# Step-by-Step Refactoring Plan

## 1. Make the global state clearer

What to do:
- Keep the current global variables, but group them together and give them explicit types where possible.
- Use `Optional[...]`-style annotations for values that start as `None`.
- Keep the configuration object separate from runtime objects like the screen, clock, and sound.

Why this helps:
- A student can immediately see which values are settings and which values are live game objects.
- Clear typing makes the code easier to understand and safer to edit.

Inline comments to add in the final code:
- Comment that some values are initialized later in `init_window()`.
- Comment that `CONFIG` stores settings while the other globals store runtime state.

## 2. Replace repeated magic numbers with named constants

What to do:
- Extract small numbers like `0.02`, `0.01`, `5`, `0.001`, and the color values into named constants near `CONFIG`.
- Keep the existing behavior by using the same numeric values.

Why this helps:
- Readers do not need to guess what each number means.
- Changing the behavior later becomes much easier because the important values live in one place.

Inline comments to add in the final code:
- Comment that these constants control jitter, AI strength, overlap safety, and colors.
- Comment that named constants improve readability by replacing “mystery numbers.”

## 3. Simplify rectangle creation

What to do:
- Keep `MovingRect.random_square()`, but make the random spawn area and size selection easier to read.
- If needed, add one tiny helper for spawn bounds so the constructor stays simple.

Why this helps:
- The code that creates new rectangles becomes easier to explain.
- It becomes clearer that spawning and motion are separate ideas.

Inline comments to add in the final code:
- Comment that this method creates new game objects with randomized starting values.
- Comment that spawn range choices help keep rectangles away from the edges at spawn time.

## 4. Make movement and wall bouncing easier to follow

What to do:
- In `move_dir(dt)`, keep the same math but make the update statements more direct and readable.
- In `wall_bounce()`, compute the next position once, then use that prediction to decide whether to flip the direction.
- Keep the clamping logic, but consider using a small helper or clearer variable names for the boundary checks.

Why this helps:
- It separates “predict position” from “apply bounce.”
- Students can see the relationship between movement, collision, and screen boundaries more clearly.

Inline comments to add in the final code:
- Comment that `dt` scales movement by frame time.
- Comment that the bounce logic first predicts the next position before changing direction.

## 5. Extract the distance helper in threat/prey search

What to do:
- Move `sq_distance_to_rect()` out of the nested function into a small top-level helper or a clearly named local helper.
- Keep the squared-distance approach, since it avoids unnecessary square roots.
- Give the helper a descriptive name that tells the reader it returns squared distance between rectangle centers.

Why this helps:
- The threat/prey function becomes easier to read because the distance math is separated from the search logic.
- The code also teaches an important concept: using squared distance is often enough for comparisons.

Inline comments to add in the final code:
- Comment that squared distance is enough when only comparing closeness.
- Comment that the loop keeps the closest larger rectangle as threat and the closest smaller rectangle as prey.

## 6. Make the steering logic more explicit

What to do:
- In `run_and_chase_vect()`, rename temporary vectors so their purpose is obvious.
- Keep the same behavior, but separate the steps into: build flee vector, build chase vector, calculate danger, blend vectors.
- Keep the clamp on `danger`.

Why this helps:
- The function currently does multiple math ideas at once.
- Breaking the logic into named steps makes vector blending easier to learn.

Inline comments to add in the final code:
- Comment that the flee vector points away from the threat.
- Comment that the chase vector points toward prey.
- Comment that `danger` controls how strongly the new direction overrides the current one.

## 7. Split the main loop into small helper actions

What to do:
- Inside `update_screen()`, extract a few tiny helpers such as:
  - one helper for drawing a rectangle,
  - one helper for updating life and respawn state,
  - one helper for drawing the FPS and rectangle counter.
- Keep `update_screen()` as the orchestration function.

Why this helps:
- The main loop becomes shorter and easier to scan.
- Each helper has one job, which is a good beginner pattern.

Inline comments to add in the final code:
- Comment that the main loop coordinates the helpers each frame.
- Comment that helper functions keep the game loop easier to read and maintain.

## 8. Improve naming and small readability issues

What to do:
- Rename variables that are vague or too short where it is safe to do so.
- Examples to consider: `rects` is fine, but `t` could become `life_ratio`, and `dt` could be explained with a comment.
- Keep function names stable unless a name clearly confuses the reader.

Why this helps:
- Better names reduce the amount of mental work needed to understand the code.
- Naming is one of the easiest ways to improve readability without changing behavior.

Inline comments to add in the final code:
- Comment when a variable name represents a ratio, a predicted position, or a frame-time value.

## 9. Add concise comments only where the code is doing a conceptually important thing

What to do:
- Add short inline comments in the final code after the refactor.
- Focus on places where the code uses an idea that a first-year student might not know yet:
  - frame-based movement,
  - squared distance comparison,
  - vector normalization,
  - danger-based blending,
  - lifespan-based color interpolation.

Why this helps:
- The final result is not just cleaner code, but also a teaching version of the code.
- Comments should explain the reason, not just restate the line.

Inline comments to add in the final code:
- Comment on what changed.
- Comment on why the change improves readability, correctness, or maintainability.
- Comment on the programming concept being used.

# Final Output Requirements (Mandatory)

When this plan is executed, the output MUST:

- Contain only the refactored code.
- Include inline comments explaining what changed.
- Include inline comments explaining why the change improves the code.
- Include inline comments that mention relevant programming concepts.
- Keep explanations concise and beginner-friendly.
- Preserve the current gameplay behavior as closely as possible.

# Key Concepts for Students

- A game loop repeats the same steps every frame: handle input, update state, draw, repeat.
- A global configuration object is a simple way to share settings.
- `pygame.Vector2` is useful because it represents direction cleanly.
- Squared distance can be enough when you only need to compare which object is closer.
- Separating one big function into small helpers makes code easier to read and debug.
- Named constants make code clearer than unexplained numbers.

# Safety Notes

- Test after each small refactor so behavior stays the same.
- Keep `init_window()` before `update_screen()` so startup still works.
- Do not change the meaning of `dt`; it still needs to represent frame time.
- Be careful not to remove the respawn sound, life timer, or bounce behavior.
- If a change makes the code harder to follow for a beginner, keep it simpler.
