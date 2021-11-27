import os

import pygame


pygame.init()

WIDTH = 900
HEIGHT = 500
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
FPS = 60
VEL = 5
BULLET_VEL = 8
MAX_BULLETS = 3
SPACESHIP_HP = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('monospace', 40)
WINNER_FONT = pygame.font.SysFont('monospace', 100)

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


def draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    red_hp_text = HEALTH_FONT.render(f'HP: {red_hp}', True, WHITE)
    yellow_hp_text = HEALTH_FONT.render(f'HP: {yellow_hp}', True, WHITE)

    WIN.blit(red_hp_text, (WIDTH - red_hp_text.get_width() - 10, 10))
    WIN.blit(yellow_hp_text, (10, 10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

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


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    text_width = draw_text.get_width()
    WIN.blit(draw_text, (WIDTH // 2 - text_width // 2, HEIGHT // 2 - text_width // 2))
    pygame.display.update()
    pygame.event.clear()
    pygame.time.delay(3000)


def main():
    red = pygame.Rect(700, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(200, HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_hp = SPACESHIP_HP
    yellow_hp = SPACESHIP_HP

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
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RALT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2,  10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_hp -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_hp -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if red_hp <= 0:
            winner_text = 'Yellow Wins!'

        if yellow_hp <= 0:
            winner_text = 'Red Wins!'

        if winner_text:
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_movement_yellow(keys_pressed, yellow)
        handle_movement_red(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp)

    main()


if __name__ == '__main__':
    main()
