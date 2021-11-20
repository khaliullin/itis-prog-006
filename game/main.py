import time

import pygame
import sys
import random

# Screen and Block size
SCREEN_HEIGHT = 480
SCREEN_WIDTH = 480
GRID_SIZE = 40

GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
INITIAL = (0, 0)

# Colors
GRID_COLOR1 = (166, 166, 166)
GRID_COLOR2 = (153, 153, 153)
FOOD_COLOR = (209, 21, 21)
FOOD_BORDER = (173, 17, 17)
SNAKE_COLOR = (21, 161, 44)
SNAKE_BORDER =(19, 145, 40)


class Snake:
    def __init__(self) -> None:
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.color = SNAKE_COLOR
        self.border = SNAKE_BORDER
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (
            (x * GRID_SIZE + cur[0]) % SCREEN_WIDTH,
            (y * GRID_SIZE + cur[1]) % SCREEN_HEIGHT
        )
        if len(self.positions) > 4 and new in self.positions[4:]:
            self.reset()
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        time.sleep(1)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = INITIAL
        self.score = 0

    def draw(self, surface):
        for p in self.positions:
            rect = pygame.Rect(p, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, self.border, rect, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

    def eat(self, food):
        if self.get_head_position() == food.position:
            self.length += 1
            self.score += 1
            food.randomize_position()
            while food.position in self.positions[1:]:
                food.randomize_position()


class Food:
    def __init__(self) -> None:
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.border = FOOD_BORDER
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, self.border, rect, 1)


def draw_grid(surface):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            if (x + y) % 2 == 0:
                pygame.draw.rect(surface, GRID_COLOR1, rect)
            else:
                pygame.draw.rect(surface, GRID_COLOR2, rect)


def main():
    pygame.init()
    pygame.display.set_caption('Snake game')

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    # https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    draw_grid(surface)

    food = Food()
    snake = Snake()

    font = pygame.font.SysFont("monospace", 16)

    while True:
        clock.tick(8)
        snake.handle_keys()
        draw_grid(surface)
        snake.move()

        food.draw(surface)
        snake.draw(surface)

        snake.eat(food)

        screen.blit(surface, (0, 0))

        text = font.render(f"Score {snake.score}", True, (0, 0, 0))
        screen.blit(text, (5, 10))

        pygame.display.update()


if __name__ == '__main__':
    main()
