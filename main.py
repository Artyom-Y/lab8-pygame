import pygame
from dataclasses import dataclass
import random
import math
from typing import Optional

#TODO real time fps counter, particle count

@dataclass
class GameConfig:
    width: int = 800
    height: int = 800
    fps: int = 60
    min_square_size: int = 5
    max_square_size: int = 20
    square_num: int = 20
    max_speed: int = 20


CONFIG = GameConfig()
SCREEN: Optional[pygame.Surface] = None
CLOCK: Optional[pygame.time.Clock] = None
IS_OPEN = False


class MovingRect(pygame.rect.Rect):
    """Subclass of pygame.rect with direction properties"""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__((x, y), (width, height))
        self.width = width
        self.height = height
        self.speed = self.set_speed()
        self.vector = self.set_vector()

    def set_speed(self):
        return random.randint(1, 5) * (CONFIG.max_speed / self.width)
    
    def set_vector(self):
        angle = random.uniform(0, math.pi*2)
        return pygame.Vector2(math.cos(angle), math.sin(angle)).normalize()
    
    def move_dir(self) -> None:
        self.x = self.x + self.vector.x * self.speed
        self.y = self.y + self.vector.y * self.speed

    def randomize_dir(self, chance: int) -> None:
        """Randomize MovingRect's direction vectors.
        :param chance: chance that the vector direction will
        change (0.0 <= chance <= 1.0)
        """
        assert chance >= 0.0 and chance <= 1.0, "chance must be within [0.0, 1.0]"

        if random.random() <= chance:
            cur_vector = self.vector
            self.vector = cur_vector.rotate_rad(random.uniform(-1, 1))

    def randomize_speed(self, chance):
        assert chance >= 0.0 and chance <= 1.0, "chance must be within [0.0, 1.0]"

        if random.random() <= chance:
            self.speed = self.set_speed()

    


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
        x = random.randint(CONFIG.width // 4, CONFIG.width // 2 + CONFIG.width // 4)
        y = random.randint(CONFIG.height // 4, CONFIG.height // 2 + CONFIG.height // 4)

        size = random.randint(CONFIG.min_square_size, CONFIG.max_square_size)

        rects.append(MovingRect(x, y, size, size))

    return rects

def update_screen() -> None:
    """Draw squares and update their position periodically"""

    global SCREEN, CLOCK
    if SCREEN is None or CLOCK is None:
        raise RuntimeError("Window was not initialized. Call init_window() first.")

    rects = create_moving_rects(CONFIG.square_num)

    while IS_OPEN:
        handle_events()
        SCREEN.fill(pygame.Color(20, 20, 20))  # to clear the screen

        for rect in rects:
            rect.move_dir()
            pygame.draw.rect(SCREEN, pygame.Color(66, 135, 245), rect)
            rect.randomize_dir(0.1)  # edit this to achieve different jitter
            rect.randomize_speed(0.01)

        pygame.display.flip()
        CLOCK.tick(CONFIG.fps)


def main() -> None:
    init_window()
    update_screen()
    pygame.quit()


if __name__ == "__main__":
    main()
