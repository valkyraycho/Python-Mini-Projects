import pygame
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")
TARGET_EVENT = pygame.USEREVENT
TARGET_INCREMENT = 400
TARGET_PADDING = 30
BG_COLOR = (0, 25, 40)
TOP_BAR_HEIGHT = 50

MAX_RADIUS = 30
GROWTH_RATE = 0.2
RED = 'red'
WHITE = 'white'
BLACK = 'black'
GREY = 'grey'
LIVES = 3

LABEL_FONT = pygame.font.SysFont('comicsans', 24)


class Target:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 0
        self.grow = True

    def update(self):
        if self.radius + GROWTH_RATE >= MAX_RADIUS:
            self.grow = False

        self.radius = self.radius + GROWTH_RATE if self.grow else self.radius - GROWTH_RATE

    def draw(self, window):
        pygame.draw.circle(window, RED, (self.x, self.y), self.radius)
        pygame.draw.circle(window, WHITE, (self.x, self.y), self.radius*0.8)
        pygame.draw.circle(window, RED, (self.x, self.y), self.radius*0.6)
        pygame.draw.circle(window, WHITE, (self.x, self.y), self.radius*0.4)

    def collided(self, x, y):
        return math.sqrt((x-self.x)**2 + (y-self.y)**2) <= self.radius


def format_time(secs):
    ms = math.floor(int(secs * 1000 % 1000) / 100)
    s = int(round(secs % 60, 1))
    min = int(secs // 60)

    return f"{min:02d}:{s:02d}:{ms:02d}"


def show_top_bar(window, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(window, GREY, (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, 'black')
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, 'black')
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, 'black')
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, 'black')

    window.blit(time_label, (5, 5))
    window.blit(speed_label, (200, 5))
    window.blit(hits_label, (450, 5))
    window.blit(lives_label, (650, 5))


def end_screen(window, elapsed_time, targets_pressed, clicks):
    window.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, WHITE)
    speed = round(targets_pressed / elapsed_time, 1)

    try:
        accuracy = round(targets_pressed / clicks * 100, 1)
    except ZeroDivisionError:
        accuracy = 0

    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, WHITE)
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, WHITE)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, WHITE)

    window.blit(time_label, (position_x(time_label), 100))
    window.blit(speed_label, (position_x(speed_label), 200))
    window.blit(hits_label, (position_x(hits_label), 300))
    window.blit(accuracy_label, (position_x(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def position_x(label):
    return WIDTH / 2 - label.get_width() / 2


def draw(window, targets):
    window.fill(BG_COLOR)
    for target in targets:
        target.draw(window)


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(
                    TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                targets.append(Target(x, y))

            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.radius <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collided(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses > LIVES:
            end_screen(WINDOW, elapsed_time, targets_pressed, clicks)

        draw(WINDOW, targets)
        show_top_bar(WINDOW, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
