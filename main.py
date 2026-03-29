import pygame
from dataclasses import dataclass
from random import uniform, randint
from typing import Optional


@dataclass
class GameConfig:
    width: int = 800
    height: int = 800
    fps: int = 60
    square_size: int = 20


CONFIG = GameConfig()
SCREEN: Optional[pygame.Surface] = None
CLOCK: Optional[pygame.time.Clock] = None
IS_OPEN = False


class MovingRect(pygame.rect.Rect):
    """Subclass of pygame.rect with direction properties"""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__((x, y), (width, height))
        self.dir_x = uniform(-1, 1)
        self.dir_y = uniform(-1, 1)

    def randomize_dir(self) -> None:
        self.dir_x = uniform(-1, 1)
        self.dir_y = uniform(-1, 1)

    def random_move(self) -> None:
        self.x = self.x + self.dir_x
        self.y = self.y + self.dir_y


def init_window() -> None:
    global SCREEN, CLOCK, IS_OPEN

    pygame.init()
    SCREEN = pygame.display.set_mode((CONFIG.width, CONFIG.height))
    pygame.display.set_caption("Moving squares")
    CLOCK = pygame.time.Clock()
    IS_OPEN = True


def handle_events() -> None:
    global IS_OPEN

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IS_OPEN = False


def create_moving_rects(n: int) -> list[MovingRect]:
    """Create n MovingRect objects with randomized starting point"""

    rects = []
    for _ in range(n):
        x = randint(CONFIG.width // 4, CONFIG.width // 2 + CONFIG.width // 4)
        y = randint(CONFIG.height // 4, CONFIG.height // 2 + CONFIG.height // 4)

        rects.append(MovingRect(x, y, CONFIG.square_size, CONFIG.square_size))

    return rects


def update_screen() -> None:
    """Draw squares and update their position periodically"""

    global SCREEN, CLOCK
    if SCREEN is None or CLOCK is None:
        raise RuntimeError("Window was not initialized. Call init_window() first.")

    rects = create_moving_rects(10)

    counter = 0
    while IS_OPEN:
        handle_events()
        SCREEN.fill(pygame.Color(20, 20, 20))  # to clear the screen

        for rect in rects:
            rect.random_move()
            pygame.draw.rect(SCREEN, pygame.Color(66, 135, 245), rect)
            if counter == 30:
                rect.randomize_dir()
        if counter == 30:
            counter = 0
        else:
            counter += 1

        pygame.display.flip()
        CLOCK.tick(CONFIG.fps)


def main() -> None:
    init_window()
    update_screen()
    pygame.quit()
    # rect = MovingRect(0, 0, 10, 10)
    # print(rect.x, rect.y)
    # rect.random_move()
    # print(rect.x, rect.y)


if __name__ == "__main__":
    main()
