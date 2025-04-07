import pygame
import random
import os

pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 24)

ASSETS = "assets"
EAT_SOUND = pygame.mixer.Sound(os.path.join(ASSETS, "eat.wav"))
CRASH_SOUND = pygame.mixer.Sound(os.path.join(ASSETS, "crash.wav"))
SNAKE_HEAD = pygame.image.load(os.path.join(ASSETS, "snake_head.png"))
SNAKE_BODY = pygame.image.load(os.path.join(ASSETS, "snake_body.png"))
FOOD_IMG = pygame.image.load(os.path.join(ASSETS, "food.png"))
BG = pygame.image.load(os.path.join(ASSETS, "bg.png"))

BLOCK_SIZE = 20
highscore_path = "highscore.txt"

if os.path.exists(highscore_path):
    with open(highscore_path, "r") as f:
        try:
            HIGH_SCORE = int(f.read())
        except:
            HIGH_SCORE = 0
else:
    HIGH_SCORE = 0

def draw_grid():
    win.blit(BG, (0, 0))

def draw_snake(snake):
    for i, block in enumerate(snake):
        img = SNAKE_HEAD if i == 0 else SNAKE_BODY
        win.blit(img, (block[0], block[1]))

def draw_food(pos):
    win.blit(FOOD_IMG, (pos[0], pos[1]))

def draw_text(text, x, y, color=(255, 255, 255)):
    label = FONT.render(text, True, color)
    win.blit(label, (x, y))

def draw_menu():
    win.fill((0, 0, 0))
    draw_text("🐍 Snake Game", WIDTH//2 - 80, HEIGHT//2 - 60)
    draw_text("Press SPACE to start", WIDTH//2 - 110, HEIGHT//2)
    draw_text("ESC to quit", WIDTH//2 - 60, HEIGHT//2 + 40)
    pygame.display.update()

def game_loop():
    global HIGH_SCORE
    snake = [(100, 100)]
    direction = (BLOCK_SIZE, 0)
    food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
    score = 0
    speed = 10
    power_up_timer = 0
    double_points = False
    running = True
    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and direction != (BLOCK_SIZE, 0):
            direction = (-BLOCK_SIZE, 0)
        if keys[pygame.K_RIGHT] and direction != (-BLOCK_SIZE, 0):
            direction = (BLOCK_SIZE, 0)
        if keys[pygame.K_UP] and direction != (0, BLOCK_SIZE):
            direction = (0, -BLOCK_SIZE)
        if keys[pygame.K_DOWN] and direction != (0, -BLOCK_SIZE):
            direction = (0, BLOCK_SIZE)
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            CRASH_SOUND.play()
            break
        if head in snake[1:]:
            CRASH_SOUND.play()
            break
        if head == food:
            EAT_SOUND.play()
            score += 2 if double_points else 1
            food = (random.randrange(0, WIDTH, BLOCK_SIZE), random.randrange(0, HEIGHT, BLOCK_SIZE))
            if random.randint(1, 5) == 3:
                double_points = True
                power_up_timer = 100
        else:
            snake.pop()
        if double_points:
            power_up_timer -= 1
            if power_up_timer <= 0:
                double_points = False
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"High Score: {HIGH_SCORE}", 10, 40)
        if double_points:
            draw_text("💥 DOUBLE POINTS!", WIDTH//2 - 100, 10, (255, 255, 0))
        pygame.display.update()
    if score > HIGH_SCORE:
        HIGH_SCORE = score
        with open(highscore_path, "w") as f:
            f.write(str(HIGH_SCORE))
    return

while True:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_loop()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()
