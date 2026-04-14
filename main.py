import pygame
from dataclasses import dataclass
import random
import math
from typing import Optional

@dataclass
class GameConfig:
    width: int = 800
    height: int = 800
    fps: int = 60
    min_square_size: int = 5
    max_square_size: int = 30
    square_num: int = 10
    max_speed: int = 5


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
        self.area = self.width * self.height
        self.life = random.randint(5, 30) * 1000 # milliseconds

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

    def randomize_speed(self, chance: int) -> None:
        """Randomize MovingRect's speed scalar.
        :param chance: chance that the speed will
        change (0.0 <= chance <= 1.0)
        """
        assert chance >= 0.0 and chance <= 1.0, "chance must be within [0.0, 1.0]"

        if random.random() <= chance:
            self.speed = self.set_speed()

    @classmethod
    def random_square(self):
        x = random.randint(CONFIG.width // 4, CONFIG.width // 2 + CONFIG.width // 4)
        y = random.randint(CONFIG.height // 4, CONFIG.height // 2 + CONFIG.height // 4)

        size = random.randint(CONFIG.min_square_size, CONFIG.max_square_size)
    
        return MovingRect(x, y, size, size)


def init_window() -> None:
    """Initialize pygame window"""
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
        rect = MovingRect.random_square()
        rects.append(rect)

    return rects

def wall_bounce(rect: MovingRect) -> MovingRect:
    """Make rectangle change direction if it's near border"""
    if rect.x <= 0 or rect.x >= CONFIG.width - rect.width:
        rect.vector.x *= -1
        rect.x = max(0, min(rect.x, CONFIG.width - rect.width))

    if rect.y <= 0 or rect.y >= CONFIG.height - rect.height:
        rect.vector.y *= -1
        rect.y = max(0, min(rect.y, CONFIG.height - rect.height))

    return rect
    
def find_threat(running_rect: MovingRect, rects: list[MovingRect]) -> MovingRect | None:
    """Given rectangle, find closest rectangle that's bigger than it"""

    def sq_distance_to_rect(other):
        return ((other.centerx - running_rect.centerx) ** 2 + (other.centery - running_rect.centery) ** 2)
    
    # by_dist_rects = sorted(rects, key=distance_to_rect)[1:] # first rect is running_rect
    running_rect_area = running_rect.area

    threat = None
    min_dist = math.inf # distance between rectangles will always be less than this

    for rect in rects:
        if rect is running_rect:
            continue
        threat_dist = sq_distance_to_rect(rect)
        if (rect.area) > running_rect_area and threat_dist < min_dist:
            threat, min_dist = rect, threat_dist
    return threat

    
def escape_threat_vector(rect: MovingRect, threat: MovingRect, k: int) -> pygame.Vector2:
    """Calculate a new vector for rect to runaway by threat.
    k is a coefficient describing how fast will rect run away"""
    away_dir = (rect.vector - threat.vector).normalize()
    dist = ((threat.x - rect.x) ** 2 + (threat.y - rect.y) ** 2) ** 0.5
    coeff = (k * (threat.width * threat.height)/(dist**2 + 0.001)) # +0.001 to prevent division by zero when rect's overlap
    if coeff > 1: # clamp
        coeff = 1
    elif coeff < 0:
        coeff = 0
    new_vect = ((1-coeff)*rect.vector + coeff*away_dir)
    return new_vect


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
            rect = wall_bounce(rect)
            rect.move_dir(dt)
            pygame.draw.rect(SCREEN, pygame.Color(66, 135, 245), rect)
            rect.randomize_dir(0.02)  # edit this to achieve different jitter
            rect.randomize_speed(0.01)

            #running away logic
            threat = find_threat(rect, rects)
            if threat:
                rect.vector = escape_threat_vector(rect, threat, 5)

            #life span feature
            rect.life -= dt
            if rect.life <= 0:
                rects.remove(rect)
                rects.append(MovingRect.random_square())
            

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
