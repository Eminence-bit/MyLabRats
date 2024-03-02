import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
SNAKE_SIZE = 20
OBSTACLE_SIZE = 20
TURQUOISE = (64, 224, 208)
DARK_PURPLE = (48, 0, 48)
MIN_FPS = 5
MAX_FPS = 15

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = TURQUOISE
        self.speed = MIN_FPS

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * SNAKE_SIZE)) % WIDTH), (cur[1] + (y * SNAKE_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
        return False

    def reset(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.speed = MIN_FPS

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], SNAKE_SIZE, SNAKE_SIZE))


# Obstacle class
class Obstacle:
    def __init__(self):
        self.position = (random.randint(0, (WIDTH // OBSTACLE_SIZE) - 1) * OBSTACLE_SIZE,
                         random.randint(0, (HEIGHT // OBSTACLE_SIZE) - 1) * OBSTACLE_SIZE)
        self.color = TURQUOISE

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], OBSTACLE_SIZE, OBSTACLE_SIZE))


# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()
    obstacle = Obstacle()

    score_font = pygame.font.SysFont("monospace", 16)
    game_over_font = pygame.font.SysFont("monospace", 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.direction != DOWN:
                        snake.direction = UP
                elif event.key == pygame.K_DOWN:
                    if snake.direction != UP:
                        snake.direction = DOWN
                elif event.key == pygame.K_LEFT:
                    if snake.direction != RIGHT:
                        snake.direction = LEFT
                elif event.key == pygame.K_RIGHT:
                    if snake.direction != LEFT:
                        snake.direction = RIGHT

        if snake.update():
            # Game over
            surface.fill(DARK_PURPLE)
            game_over_text = game_over_font.render("Game Over", True, TURQUOISE)
            surface.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))
            score_text = score_font.render(f"Score: {snake.length - 1}", True, TURQUOISE)
            surface.blit(score_text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.update()
            
            time.sleep(2)  # Pause for 2 seconds
            snake.reset()

        # Check for collisions with obstacles
        if snake.get_head_position() == obstacle.position:
            snake.length += 1
            obstacle = Obstacle()

            # Increase speed if not at maximum
            if snake.speed < MAX_FPS:
                snake.speed += 1

        # Check for collisions with walls
        if snake.get_head_position()[0] < 0 or snake.get_head_position()[0] >= WIDTH or \
           snake.get_head_position()[1] < 0 or snake.get_head_position()[1] >= HEIGHT:
            # Game over
            surface.fill(DARK_PURPLE)
            game_over_text = game_over_font.render("Game Over", True, TURQUOISE)
            surface.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))
            score_text = score_font.render(f"Score: {snake.length - 1}", True, TURQUOISE)
            surface.blit(score_text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.update()
            
            time.sleep(2)  # Pause for 2 seconds
            snake.reset()

        surface.fill(DARK_PURPLE)
        snake.render(surface)
        obstacle.render(surface)

        score_text = score_font.render(f"Score: {snake.length - 1}", True, TURQUOISE)
        surface.blit(score_text, (10, 10))

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(snake.speed)

if __name__ == "__main__":
    main()
