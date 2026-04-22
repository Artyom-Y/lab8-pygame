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


CONFIG: GameConfig = GameConfig()
SCREEN: pygame.Surface = None
CLOCK: pygame.time.Clock = None
IS_OPEN: bool = False
FONT: pygame.font.SysFont = None
REBIRTH_SOUND: pygame.mixer.Sound = None
START_COLOR: pygame.Color = None
END_COLOR: pygame.Color = None

class MovingRect(pygame.rect.Rect):
    """Subclass of pygame.rect with direction properties"""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__((x, y), (width, height))
        self.speed = self.set_speed()
        self.vector = self.set_vector()
        self.area = self.width * self.height
        self.max_life = random.randint(10, 25) * 1000 # milliseconds, used for calculating color
        self.curr_life = self.max_life
        self.color = START_COLOR


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

    @staticmethod
    def random_square():
        x = random.randint(CONFIG.width // 4, CONFIG.width // 2 + CONFIG.width // 4)
        y = random.randint(CONFIG.height // 4, CONFIG.height // 2 + CONFIG.height // 4)

        size = random.randint(CONFIG.min_square_size, CONFIG.max_square_size)
    
        return MovingRect(x, y, size, size)
    
    @staticmethod
    def lerp_color(first:pygame.Color, second:pygame.Color, t: float) -> pygame.Color:
        """Linear interpolation between two colors based on coefficient t.
        Credits to https://www.reddit.com/r/pygame/comments/a26i7u/comment/eawhe0a"""
        return pygame.Color(*[int((1 - t) * v0 + t * v1) for v0, v1 in zip(first, second)])


def init_window() -> None:
    """Initialize pygame window"""
    global SCREEN, CLOCK, IS_OPEN, FONT, START_COLOR, END_COLOR, REBIRTH_SOUND

    pygame.init()
    SCREEN = pygame.display.set_mode((CONFIG.width, CONFIG.height))
    pygame.display.set_caption("Moving squares")
    CLOCK = pygame.time.Clock()
    FONT = pygame.font.SysFont("Arial", 18)
    pygame.mixer.init()
    REBIRTH_SOUND = pygame.mixer.Sound("media/pop.mp3")
    REBIRTH_SOUND.set_volume(0.5)
    START_COLOR = pygame.Color(66, 135, 245)
    END_COLOR = pygame.Color(245, 66, 66)

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
        rect = MovingRect.random_square()
        rects.append(rect)

    return rects

def wall_bounce(rect: MovingRect, dt: int) -> MovingRect:
    """Make rectangle change direction if it's near border"""
    new_x = rect.x + rect.vector.x * rect.speed * dt
    new_y = rect.y + rect.vector.y * rect.speed * dt
    if new_x <= 0 or new_x + rect.width >= CONFIG.width:
        rect.vector.x *= -1
        rect.x = max(0, min(rect.x, CONFIG.width - rect.width))

    if new_y <= 0 or new_y + rect.height >= CONFIG.height:
        rect.vector.y *= -1
        rect.y = max(0, min(rect.y, CONFIG.height - rect.height))

    return rect
    
def find_threat_and_prey(running_rect: MovingRect, rects: list[MovingRect]) -> tuple[MovingRect | None, MovingRect | None]:
    """Given rectangle, find closest rectangle that's bigger than it (threat) and smaller (prey)"""

    def sq_distance_to_rect(other):
        return ((other.centerx - running_rect.centerx) ** 2 + (other.centery - running_rect.centery) ** 2)
    
    running_rect_area = running_rect.area

    threat = None
    min_threat_dist = math.inf # distance between rectangles will always be less than this
    prey = None
    min_prey_dist = math.inf

    for rect in rects:
        if rect is running_rect:
            continue
        dist = sq_distance_to_rect(rect)
        if rect.area > running_rect_area and dist < min_threat_dist:
            threat, min_threat_dist = rect, dist
        elif rect.area < running_rect_area and dist < min_prey_dist:
            prey, min_prey_dist = rect, dist

    return threat, prey

    
def run_and_chase_vect(rect: MovingRect, threat: MovingRect | None, prey: MovingRect | None, k: int) -> pygame.Vector2:
    """Calculate a new vector for rect to runaway from threat and chase the prey.
    k is a coefficient describing how fast will rect run away.
    Running away is prioritized to chasing. If the square has no threats, it's only concerned with chasing
    (and vice versa for the smallest one)"""

    run_vect = pygame.Vector2()
    chase_vect = pygame.Vector2()
    danger = 0.5 # the biggest square will always lerp into new vector at this rate

    if threat:
        run_vect.update(rect.x - threat.x, rect.y - threat.y)

        dist = run_vect.length_squared()
        danger = (k * (threat.width * threat.height)/(dist + 0.001)) # +0.001 to prevent division by zero when rect's overlap
        if danger > 1: # clamp
            danger = 1
        elif danger < 0:
            danger = 0

    if prey:
        chase_vect.update(prey.x - rect.x, prey.y - rect.y)

    new_vect = (run_vect + chase_vect).normalize()

    return (1-danger) * rect.vector + danger * new_vect

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

        alive = []
        respawn_count = 0

        for rect in rects:
            rect = wall_bounce(rect, dt)
            rect.move_dir(dt)

            t = rect.curr_life / rect.max_life
            rect.color = MovingRect.lerp_color(END_COLOR, START_COLOR, t)
            pygame.draw.rect(SCREEN, rect.color, rect)

            rect.randomize_dir(0.02)  # edit this to achieve different jitter
            rect.randomize_speed(0.01)

            #running away/chasing after logic
            threat, prey = find_threat_and_prey(rect, rects)
            rect.vector = run_and_chase_vect(rect, threat, prey, 5)

            #life span feature
            rect.curr_life -= dt
            if rect.curr_life <= 0:
                respawn_count += 1
                REBIRTH_SOUND.play()
            else:
                alive.append(rect)

        rects = alive

        for _ in range(respawn_count):
            rects.append(MovingRect.random_square())
            

        # interface
        fps_counter = pygame.font.Font.render(FONT, f"FPS: {CLOCK.get_fps():.2f}", True, (255, 255, 255))
        rect_counter = pygame.font.Font.render(FONT, f"Total rects: {CONFIG.square_num}", True, (255, 255, 255))

        SCREEN.blit(fps_counter, (10, 10))
        SCREEN.blit(rect_counter, (10, 30))

        pygame.display.flip()
        


def main() -> None:
    init_window()
    update_screen()
    pygame.quit()


if __name__ == "__main__":
    main()
