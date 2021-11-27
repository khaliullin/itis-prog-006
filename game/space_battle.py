import os

import pygame

WIDTH = 900
HEIGHT = 500
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
FPS = 60
VEL = 5
MAX_BULLETS = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_yellow.png')
)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_red.png')
)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90
)
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270
)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'space.png')),
    (WIDTH, HEIGHT)
)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space battle")


def draw_window(red, yellow):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    pygame.display.update()


def handle_movement_yellow(keys_pressed, spaceship):
    if keys_pressed[pygame.K_a] and spaceship.x - VEL > 0:
        spaceship.x -= VEL
    if keys_pressed[pygame.K_d] and spaceship.x + VEL + spaceship.width < BORDER.x:
        spaceship.x += VEL
    if keys_pressed[pygame.K_w] and spaceship.y - VEL > 0:
        spaceship.y -= VEL
    if keys_pressed[pygame.K_s] and spaceship.y + VEL + spaceship.height < HEIGHT - 15:
        spaceship.y += VEL


def handle_movement_red(keys_pressed, spaceship):
    if keys_pressed[pygame.K_LEFT] and spaceship.x - VEL > BORDER.x + BORDER.width:
        spaceship.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and spaceship.x + VEL + spaceship.width < WIDTH:
        spaceship.x += VEL
    if keys_pressed[pygame.K_UP] and spaceship.y - VEL > 0:
        spaceship.y -= VEL
    if keys_pressed[pygame.K_DOWN] and spaceship.y + VEL + spaceship.height < HEIGHT - 15:
        spaceship.y += VEL


def main():
    red = pygame.Rect(700, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(200, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2,  10, 5)
                yellow_bullets.append(bullet)
            if event.key == pygame.K_RALT and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red.x, red.y + red.height // 2,  10, 5)
                red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        handle_movement_yellow(keys_pressed, yellow)
        handle_movement_red(keys_pressed, red)

        draw_window(red, yellow)
        print(yellow_bullets)




if __name__ == '__main__':
    main()
