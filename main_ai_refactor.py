from __future__ import annotations
import pygame
from dataclasses import dataclass
import random
import math
from typing import Optional

# Named constants replace magic numbers so behavior is easier to tune and explain.
LIFE_MIN_SECONDS = 10
LIFE_MAX_SECONDS = 25
LIFE_TO_MS = 1000

JITTER_DIRECTION_CHANCE = 0.02
JITTER_SPEED_CHANCE = 0.01
AI_DANGER_STRENGTH = 5
AI_BIGGEST_RECT_BASE_DANGER = 0.5
AI_DISTANCE_EPSILON = 0.001

BACKGROUND_COLOR = pygame.Color(20, 20, 20)
UI_TEXT_COLOR = (255, 255, 255)
START_COLOR_RGB = (66, 135, 245)
END_COLOR_RGB = (245, 66, 66)

REBIRTH_SOUND_PATH = "media/pop.mp3"
REBIRTH_SOUND_VOLUME = 0.5

@dataclass
class GameConfig:
    width: int = 800
    height: int = 800
    fps: int = 60
    min_square_size: int = 5
    max_square_size: int = 30
    square_num: int = 10
    max_speed: int = 7


CONFIG: GameConfig = GameConfig()
# Runtime globals are initialized in init_window(); Optional types make that explicit.
SCREEN: Optional[pygame.Surface] = None
CLOCK: Optional[pygame.time.Clock] = None
IS_OPEN: bool = False
FONT: Optional[pygame.font.Font] = None
REBIRTH_SOUND: Optional[pygame.mixer.Sound] = None
START_COLOR: Optional[pygame.Color] = None
END_COLOR: Optional[pygame.Color] = None


def clamp(value: float, low: float, high: float) -> float:
    """Clamp a numeric value into [low, high]."""
    return max(low, min(value, high))


def squared_center_distance(first: pygame.rect.Rect, second: pygame.rect.Rect) -> float:
    """Squared distance is enough when we only compare which object is closer."""
    dx = first.centerx - second.centerx
    dy = first.centery - second.centery
    return (dx * dx) + (dy * dy)


def draw_ui_overlay() -> None:
    """Draw small text HUD elements; extracted to keep update loop focused."""
    if SCREEN is None or CLOCK is None or FONT is None:
        return

    fps_counter = pygame.font.Font.render(FONT, f"FPS: {CLOCK.get_fps():.2f}", True, UI_TEXT_COLOR)
    rect_counter = pygame.font.Font.render(FONT, f"Total rects: {CONFIG.square_num}", True, UI_TEXT_COLOR)
    SCREEN.blit(fps_counter, (10, 10))
    SCREEN.blit(rect_counter, (10, 30))


def update_life_and_respawn(rect: MovingRect, dt_ms: int) -> bool:
    """Update lifespan and return whether rectangle stays alive this frame."""
    rect.curr_life -= dt_ms
    if rect.curr_life <= 0:
        if REBIRTH_SOUND is not None:
            REBIRTH_SOUND.play()
        return False
    return True

class MovingRect(pygame.rect.Rect):
    """Subclass of pygame.rect with direction properties"""

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__((x, y), (width, height))
        self.speed = self.set_speed()
        self.vector = self.set_vector()
        self.area = self.width * self.height
        self.max_life = random.randint(LIFE_MIN_SECONDS, LIFE_MAX_SECONDS) * LIFE_TO_MS
        self.curr_life = self.max_life
        self.color = START_COLOR


    def set_speed(self) -> float:
        return random.randint(CONFIG.max_speed // 2, CONFIG.max_speed) / self.width
    
    def set_vector(self) -> pygame.Vector2:
        angle = random.uniform(0, math.pi * 2)
        # Unit vectors separate direction from speed, which simplifies steering math.
        return pygame.Vector2(math.cos(angle), math.sin(angle)).normalize()
    
    def move_dir(self, dt_ms: int) -> None:
        # Frame-time scaling keeps movement consistent across different frame durations.
        self.x += self.vector.x * self.speed * dt_ms
        self.y += self.vector.y * self.speed * dt_ms

    def randomize_dir(self, chance: float) -> None:
        """Randomize MovingRect's direction vectors.
        :param chance: chance that the vector direction will
        change (0.0 <= chance <= 1.0)
        """
        assert chance >= 0.0 and chance <= 1.0, "chance must be within [0.0, 1.0]"

        if random.random() <= chance:
            self.vector = self.vector.rotate_rad(random.uniform(-1, 1))

    def randomize_speed(self, chance: float) -> None:
        """Randomize MovingRect's speed scalar.
        :param chance: chance that the speed will
        change (0.0 <= chance <= 1.0)
        """
        assert chance >= 0.0 and chance <= 1.0, "chance must be within [0.0, 1.0]"

        if random.random() <= chance:
            self.speed = self.set_speed()

    @staticmethod
    def random_square() -> MovingRect:
        # Spawn ranges keep new rectangles away from borders at creation time.
        x_min = CONFIG.width // 4
        x_max = CONFIG.width // 2 + CONFIG.width // 4
        y_min = CONFIG.height // 4
        y_max = CONFIG.height // 2 + CONFIG.height // 4

        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)

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
    REBIRTH_SOUND = pygame.mixer.Sound(REBIRTH_SOUND_PATH)
    REBIRTH_SOUND.set_volume(REBIRTH_SOUND_VOLUME)
    START_COLOR = pygame.Color(*START_COLOR_RGB)
    END_COLOR = pygame.Color(*END_COLOR_RGB)

    IS_OPEN = True

def handle_events() -> None:
    global IS_OPEN

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IS_OPEN = False


def create_moving_rects(n: int) -> list[MovingRect]:
    """Create n MovingRect objects with randomized starting point"""

    rects: list[MovingRect] = []
    for _ in range(n):
        rect = MovingRect.random_square()
        rects.append(rect)

    return rects

def wall_bounce(rect: MovingRect, dt_ms: int) -> MovingRect:
    """Predict next position first, then reflect direction when crossing borders."""
    new_x = rect.x + rect.vector.x * rect.speed * dt_ms
    new_y = rect.y + rect.vector.y * rect.speed * dt_ms
    if new_x <= 0 or new_x + rect.width >= CONFIG.width:
        rect.vector.x *= -1
        rect.x = int(clamp(rect.x, 0, CONFIG.width - rect.width))

    if new_y <= 0 or new_y + rect.height >= CONFIG.height:
        rect.vector.y *= -1
        rect.y = int(clamp(rect.y, 0, CONFIG.height - rect.height))

    return rect
    
def find_threat_and_prey(running_rect: MovingRect, rects: list[MovingRect]) -> tuple[MovingRect | None, MovingRect | None]:
    """Given rectangle, find closest rectangle that's bigger than it (threat) and smaller (prey)"""
    
    running_rect_area = running_rect.area

    threat: Optional[MovingRect] = None
    min_threat_dist = math.inf
    prey: Optional[MovingRect] = None
    min_prey_dist = math.inf

    for rect in rects:
        if rect is running_rect:
            continue

        dist = squared_center_distance(running_rect, rect)
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

    flee_vector = pygame.Vector2()
    chase_vector = pygame.Vector2()
    danger = AI_BIGGEST_RECT_BASE_DANGER

    if threat:
        # Flee vector points away from the threat rectangle.
        flee_vector.update(rect.x - threat.x, rect.y - threat.y)

        dist = flee_vector.length_squared()
        danger = (k * (threat.width * threat.height)) / (dist + AI_DISTANCE_EPSILON)
        # Danger blending controls how strongly new steering overrides old direction.
        danger = clamp(danger, 0, 1)

    if prey:
        # Chase vector points toward prey when there is no immediate danger.
        chase_vector.update(prey.x - rect.x, prey.y - rect.y)

    blended_target_vector = flee_vector + chase_vector
    if blended_target_vector.length():
        blended_target_vector = blended_target_vector.normalize()

    return ((1 - danger) * rect.vector) + (danger * blended_target_vector)


def apply_rect_behaviors(rect: MovingRect, rects: list[MovingRect], dt_ms: int) -> bool:
    """Apply one frame of physics, AI, color, and life update for a rectangle."""
    global SCREEN
    if SCREEN is None or START_COLOR is None or END_COLOR is None:
        return False

    rect = wall_bounce(rect, dt_ms)
    rect.move_dir(dt_ms)

    life_ratio = rect.curr_life / rect.max_life
    rect.color = MovingRect.lerp_color(END_COLOR, START_COLOR, life_ratio)
    pygame.draw.rect(SCREEN, rect.color, rect)

    rect.randomize_dir(JITTER_DIRECTION_CHANCE)
    rect.randomize_speed(JITTER_SPEED_CHANCE)

    threat, prey = find_threat_and_prey(rect, rects)
    rect.vector = run_and_chase_vect(rect, threat, prey, AI_DANGER_STRENGTH)

    return update_life_and_respawn(rect, dt_ms)


def respawn_rects(rects: list[MovingRect], respawn_count: int) -> list[MovingRect]:
    """Keep population stable by respawning dead rectangles."""
    for _ in range(respawn_count):
        rects.append(MovingRect.random_square())
    return rects

def update_screen() -> None:
    """Draw squares and update their position periodically"""

    global SCREEN, CLOCK
    if SCREEN is None or CLOCK is None:
        raise RuntimeError("Window was not initialized. Call init_window() first.")

    rects = create_moving_rects(CONFIG.square_num)

    while IS_OPEN:
        handle_events()
        SCREEN.fill(BACKGROUND_COLOR)
        dt_ms = CLOCK.tick(CONFIG.fps)

        alive: list[MovingRect] = []
        respawn_count = 0

        for rect in rects:
            if apply_rect_behaviors(rect, rects, dt_ms):
                alive.append(rect)
            else:
                respawn_count += 1

        rects = respawn_rects(alive, respawn_count)
        draw_ui_overlay()

        pygame.display.flip()
        


def main() -> None:
    init_window()
    update_screen()
    pygame.quit()


if __name__ == "__main__":
    main()
