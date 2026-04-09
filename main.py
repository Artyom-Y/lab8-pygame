import pygame
from dataclasses import dataclass
import random
import math
import time
from typing import Optional

@dataclass
class GameConfig:
    width: int = 800
    height: int = 800
    fps: int = 60
    min_square_size: int = 5
    max_square_size: int = 30
    square_num: int = 10
    max_speed: int = 8


CONFIG = GameConfig()
SCREEN: Optional[pygame.Surface] = None
CLOCK: Optional[pygame.time.Clock] = None
IS_OPEN = False
FONT: Optional[pygame.font.SysFont] = None


class MovingRect(pygame.rect.Rect):
    """Subclass of pygame.rect with direction properties"""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__((x, y), (width, height))
        self.speed = self.set_speed()
        self.vector = self.set_vector()
        self.turning = True
        self.turn_time = time.monotonic()

    def set_speed(self):
        return (CONFIG.max_speed / self.width)
    
    def set_vector(self):
        angle = random.uniform(0, math.pi*2)
        return pygame.Vector2(math.cos(angle), math.sin(angle)).normalize()
    
    def move_dir(self, dt) -> None:
        self.x = self.x + self.vector.x * self.speed * dt
        self.y = self.y + self.vector.y * self.speed * dt

    def randomize_dir(self, chance: int) -> None:
        """Randomize MovingRect's direction vectors.
        :param chance: chance that the vector direction will
        change (0.0 <= chance <= 1.0)
        """
        assert chance >= 0.0 and chance <= 1.0, "chance must be within [0.0, 1.0]"

        if random.random() <= chance:
            self.vector.rotate_rad(random.uniform(-1, 1))

    def randomize_speed(self, chance):
        assert chance >= 0.0 and chance <= 1.0, "chance must be within [0.0, 1.0]"

        if random.random() <= chance:
            self.speed = self.set_speed()
    


def init_window() -> None:
    global SCREEN, CLOCK, IS_OPEN, FONT

    pygame.init()
    SCREEN = pygame.display.set_mode((CONFIG.width, CONFIG.height))
    pygame.display.set_caption("Moving squares")
    CLOCK = pygame.time.Clock()
    IS_OPEN = True
    FONT = pygame.font.SysFont("Arial", 18)

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

def wall_bounce(rect: MovingRect, sec: int) -> MovingRect:
    cur_vector = rect.vector

    # NOTE: rects would get stuck in a loop of flipping directions when near borders
    # So I made bouncing have a little cooldown to prevent that (specified by sec parameter)
    cur_time = time.monotonic()
    if cur_time - rect.turn_time >= sec:
        rect.turning = True

    if not ((rect.x > rect.width//2 and rect.x < CONFIG.width - rect.width//2) and (rect.y > rect.height//2 and rect.y < CONFIG.height - rect.height//2)):
        if rect.turning: # so that rect won't get stuck in a loop of flipping directions
            rand_angle = random.uniform(-0.5, 0.5)
            cur_vector = cur_vector.rotate_rad(math.pi + rand_angle) # randomize bounce direction
            rect.vector = cur_vector

            rect.turn_time = time.monotonic()
            rect.turning = False

    return rect
    
def find_threat(rect, rects):
    """Given rectangle, find closest rectangle that's bigger than it"""
    other_rects = rects.copy()
    other_rects.remove(rect)

    def distance_to_rect(other):
        return ((other.x - rect.x) ** 2 + (other.y - rect.y) ** 2) ** 0.5
    
    bigger_rects = []
    rect_area = rect.width * rect.height

    for other_rect in other_rects:
        if (other_rect.width * other_rect.height) > rect_area:
            bigger_rects.append(other_rect)

    if bigger_rects:
        bigger_rects = sorted(bigger_rects, key=distance_to_rect)
        return bigger_rects[0]
    else: 
        return None # The biggest rectangle doesn't have to escape anyone


def update_screen() -> None:
    """Draw squares and update their position periodically"""

    global SCREEN, CLOCK
    if SCREEN is None or CLOCK is None:
        raise RuntimeError("Window was not initialized. Call init_window() first.")

    rects = create_moving_rects(CONFIG.square_num)

    while IS_OPEN:
        handle_events()
        SCREEN.fill(pygame.Color(20, 20, 20))  # to clear the screen
        dt = CLOCK.tick(CONFIG.fps)

        for rect in rects:
            rect = wall_bounce(rect, 0.5)
            rect.move_dir(dt)
            pygame.draw.rect(SCREEN, pygame.Color(66, 135, 245), rect)
            rect.randomize_dir(0.02)  # edit this to achieve different jitter
            rect.randomize_speed(0.01)

            #running away logic
            threat = find_threat(rect, rects)
            if threat:
                away_dir = (rect.vector - threat.vector).normalize()
                dist = ((threat.x - rect.x) ** 2 + (threat.y - rect.y) ** 2) ** 0.5
                coeff = ((threat.width * threat.height)/(dist**2 + 1)) # +1 to prevent division by zero when rect overlap
                if coeff > 1: # clamp
                    coeff = 1
                elif coeff < 0:
                    coeff = 0
                new_vect = ((1-coeff)*rect.vector + coeff*away_dir)
                rect.vector = new_vect
            

        # interface
        fps_counter = pygame.font.Font.render(FONT, f"FPS: {CLOCK.get_fps():.2f}", True, (255, 255, 255))
        rect_counter = pygame.font.Font.render(FONT, f"Rects: {CONFIG.square_num}", True, (255, 255, 255))

        SCREEN.blit(fps_counter, (10, 10))
        SCREEN.blit(rect_counter, (10, 30))

        pygame.display.flip()
        


def main() -> None:
    init_window()
    update_screen()
    pygame.quit()


if __name__ == "__main__":
    main()
