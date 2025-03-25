import pygame
import random
import os
import math
from collections import deque

pygame.init()

# === Constants ===
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 16
GOAL_SCORE = 19
BASE_BALL_SPEED = 4 * 1.3
BASE_PADDLE_SPEED = 8 * 1.3
FPS = 60
MAX_MISSES = 3

TEXTURE_DIR = "textures"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rainbow Ball Catcher")
font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()

# === Load Texture Helper ===
def load_texture(filename, target_height=None, target_width=None, fallback_color=(200, 0, 0), alpha=True):
    path = os.path.join(TEXTURE_DIR, filename)
    try:
        image = pygame.image.load(path)
        image = image.convert_alpha() if alpha else image.convert()
        if target_height or target_width:
            w, h = image.get_size()
            if target_height and not target_width:
                scale = target_height / h
                new_size = (int(w * scale), target_height)
            elif target_width and not target_height:
                scale = target_width / w
                new_size = (target_width, int(h * scale))
            else:
                scale = min(target_width / w, target_height / h)
                new_size = (int(w * scale), int(h * scale))
            image = pygame.transform.smoothscale(image, new_size)
        return image
    except Exception as e:
        print(f"[WARNING] Could not load '{filename}': {e}")
        surf = pygame.Surface((target_width or 40, target_height or 40), pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf

# === Load Textures ===
background_img = load_texture("Background.png", target_width=WIDTH)
background_img.set_alpha(76)  # 30% opacity

goku_img = load_texture("Goku.png.png", target_width=WIDTH, target_height=HEIGHT)
sun_img = load_texture("Sun.png", target_height=120)
paddle_img = load_texture("Paddel.png", target_height=40)

battery_textures = {
    0: load_texture("Batt_0.png", 200 * 2.5, 50 * 2.5),
    25: load_texture("Batt_25.png", 200 * 2.5, 50 * 2.5),
    50: load_texture("Batt_50.png", 200 * 2.5, 50 * 2.5),
    75: load_texture("Batt_75.png", 200 * 2.5, 50 * 2.5),
    100: load_texture("Batt_100.png", 200 * 2.5, 50 * 2.5),
}

ball_textures = {
    c: load_texture(f"Ball_{c}.png", target_height=60)
    for c in ["R", "O", "Y", "G", "B", "I", "V"]
}

# === Classes ===
class VPaddle:
    def __init__(self):
        self.width = int(160 * 1.5)
        self.height = int(75 * 1.5)
        self.x = (WIDTH - self.width) // 2
        self.speed = BASE_PADDLE_SPEED
        self.image = pygame.transform.scale(paddle_img, (self.width, self.height))

    def move(self, direction):
        if direction == "LEFT":
            self.x -= self.speed
        elif direction == "RIGHT":
            self.x += self.speed
        self.x = max(0, min(WIDTH - self.width, self.x))

    def draw(self):
        tip_x = self.x + self.width // 2
        tip_y = HEIGHT - 20
        screen.blit(self.image, (self.x, HEIGHT - self.height))
        pygame.draw.line(screen, (0, 0, 0), (self.x, HEIGHT - self.height), (tip_x, tip_y), 10)
        pygame.draw.line(screen, (0, 0, 0), (self.x + self.width, HEIGHT - self.height), (tip_x, tip_y), 10)

class Sun:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 60
        self.radius = 60
        self.image = sun_img

    def draw(self):
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))

class Ball:
    def __init__(self, sun):
        self.sun = sun
        self.afterimages = deque(maxlen=8)
        self.reset()

    def reset(self):
        self.color_key = random.choice(list(ball_textures.keys()))
        self.image = ball_textures[self.color_key]
        self.x = self.sun.x
        self.y = self.sun.y + self.sun.radius
        angle = random.uniform(math.radians(30), math.radians(150))
        speed = BASE_BALL_SPEED + (speed_score * 0.05)
        self.x_speed = math.cos(angle) * speed * random.choice([-1, 1])
        self.y_speed = math.sin(angle) * speed
        self.afterimages.clear()

    def move(self):
        self.afterimages.appendleft((self.x, self.y))
        self.x += self.x_speed
        self.y += self.y_speed
        if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= WIDTH:
            self.x_speed *= -1
        if self.y - BALL_RADIUS <= 0:
            self.y_speed *= -1

    def draw(self):
        angle = math.degrees(math.atan2(-self.y_speed, self.x_speed))
        for idx, (x, y) in enumerate(list(self.afterimages)[::-1]):
            alpha = int(255 * (0.3 * (idx + 1) / len(self.afterimages)))
            faded = self.image.copy()
            faded.set_alpha(alpha)
            rotated = pygame.transform.rotate(faded, angle)
            rect = rotated.get_rect(center=(x, y))
            screen.blit(rotated, rect)
        rotated_main = pygame.transform.rotate(self.image, angle)
        rect = rotated_main.get_rect(center=(self.x, self.y))
        screen.blit(rotated_main, rect)

    def is_inside_v(self, v_x, v_width, v_height):
        tip_x = v_x + v_width // 2
        tip_y = HEIGHT - 20
        left = (v_x, HEIGHT - v_height)
        right = (v_x + v_width, HEIGHT - v_height)
        pt = (self.x, self.y)

        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - \
                   (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(pt, left, (tip_x, tip_y)) < 0.0
        b2 = sign(pt, (tip_x, tip_y), right) < 0.0
        b3 = sign(pt, right, left) < 0.0

        return (b1 == b2) and (b2 == b3)

# === Game Initialization ===
def reset_game():
    global balls, score, speed_score, misses
    score = 0
    speed_score = 0
    misses = 0
    balls = [Ball(sun)]

sun = Sun()
paddle = VPaddle()
reset_game()

# === Game Loop ===
running = True
while running:
    screen.fill((0, 0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: paddle.move("LEFT")
    if keys[pygame.K_RIGHT]: paddle.move("RIGHT")

    sun.draw()
    paddle.draw()

    for ball in balls[:]:
        ball.move()
        ball.draw()

        if ball.is_inside_v(paddle.x, paddle.width, paddle.height):
            gained = 2 if ball.color_key in ["G", "B", "V"] else 1
            score += gained
            speed_score += gained
            ball.reset()

            # Spawn extra ball every 10 speed points
            if speed_score % 10 == 0:
                balls.append(Ball(sun))

        elif ball.y > HEIGHT:
            ball.reset()
            misses += 1
            if misses >= MAX_MISSES:
                reset_game()

    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (20, 20))

    percent = (score / GOAL_SCORE) * 100
    if percent >= 100:
        bar_img = battery_textures[100]
    elif percent >= 75:
        bar_img = battery_textures[75]
    elif percent >= 50:
        bar_img = battery_textures[50]
    elif percent >= 25:
        bar_img = battery_textures[25]
    else:
        bar_img = battery_textures[0]
    screen.blit(bar_img, (30, 80))

    screen.blit(background_img, (0, 0))

    if score >= GOAL_SCORE:
        screen.blit(goku_img, (0, 0))
        win_text = font.render("You Win!", True, (255, 255, 255))
        screen.blit(win_text, (WIDTH // 2 - 60, HEIGHT // 2 + 100))
        pygame.display.update()
        pygame.time.wait(3000)
        reset_game()


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
