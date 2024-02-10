
# import sys module
import pygame
import sys
import asyncio
import random
  

# Game grid dimensions
GRID_WIDTH = 400
GRID_HEIGHT = 400
CELL_SIZE = 10

# UI dimesions
LIVES_HEIGHT = 20
GAME_OVER_HEIGHT = 20
UI_HEIGHT = LIVES_HEIGHT + GAME_OVER_HEIGHT
UI_X_OFFSET = 10

# Screen dimensions
SCREEN_WIDTH = GRID_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT + UI_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# User-controlled cell color
PLAYER_COLOR = BLUE

# Goal cell color
GOAL_COLOR = GREEN

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Conway's Game of Life with User Control")


def apply_rule(grid, x, y):
    live_neighbors = 0
    for neighbor_y in range(max(0, y - 1), min(GRID_HEIGHT // CELL_SIZE, y + 2)):
        for neighbor_x in range(max(0, x - 1), min(GRID_WIDTH // CELL_SIZE, x + 2)):
            if not (neighbor_y == y and neighbor_x == x) and grid[neighbor_y][neighbor_x]:
                live_neighbors += 1

    # Apply rules
    if live_neighbors == 3:
        return True  # Alive
    elif live_neighbors == 2:
        return grid[y][x] # Keep state
    else:
        return False # Dead


def draw_initial_screen(font, grid, player_x, player_y, goal_x, goal_y):
    draw_grid(grid, player_x, player_y, goal_x, goal_y)
    intro_text = font.render("""You are BLUE, the goal is GREEN""", True, (0, 255, 255))
    screen.blit(intro_text, (UI_X_OFFSET, GRID_HEIGHT))
    pygame.display.flip()


def draw_grid(grid, player_x, player_y, goal_x, goal_y):
    # Draw grid
    screen.fill(BLACK)
    for y in range(GRID_HEIGHT // CELL_SIZE):
        for x in range(GRID_WIDTH // CELL_SIZE):
            color = WHITE if grid[y][x] else BLACK
            if x == player_x and y == player_y:
                color = PLAYER_COLOR
            elif x == goal_x and y == goal_y:
                color = GOAL_COLOR
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


async def main():
    lives = 10

    # Create font object
    font = pygame.font.SysFont(None, 36)

    # Initialize game grid
    grid = [[bool(random.randint(0, 1)) for _ in range(GRID_WIDTH // CELL_SIZE)] for _ in range(GRID_HEIGHT // CELL_SIZE)]

    # Player cell position
    player_x, player_y = GRID_WIDTH // CELL_SIZE // 2, GRID_HEIGHT // CELL_SIZE // 2
    grid[player_y][player_x] = True

    # Goal position
    goal_x, goal_y = random.randint(0, GRID_WIDTH // CELL_SIZE - 1), random.randint(0, GRID_HEIGHT // CELL_SIZE - 1)

    # Initial render
    draw_initial_screen(font, grid, player_x, player_y, goal_x, goal_y)

    running = True
    playing = True
    while running:
        # Handle events
        had_interaction = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                running = False
            elif event.type == pygame.KEYDOWN:
                had_interaction = True
                if event.key == pygame.K_UP:
                    player_y = max(0, player_y - 1)
                elif event.key == pygame.K_DOWN:
                    player_y = min(GRID_HEIGHT // CELL_SIZE - 1, player_y + 1)
                elif event.key == pygame.K_LEFT:
                    player_x = max(0, player_x - 1)
                elif event.key == pygame.K_RIGHT:
                    player_x = min(GRID_WIDTH // CELL_SIZE - 1, player_x + 1)

        if had_interaction and playing:
            # Copy grid for updates
            new_grid = grid

            # Apply Conway's rules
            for y in range(GRID_HEIGHT // CELL_SIZE):
                for x in range(GRID_WIDTH // CELL_SIZE):
                    new_grid[y][x] = apply_rule(grid, x, y)

            if not apply_rule(new_grid, player_x, player_y):
                lives -= 1

            # Update grid and player position
            grid = new_grid
            grid[player_y][player_x] = True

            draw_grid(grid, player_x, player_y, goal_x, goal_y)

            # Render lives text
            score_text = font.render("Lives: " + str(lives), True, (0, 255, 255))
            screen.blit(score_text, (UI_X_OFFSET, GRID_HEIGHT))

            if player_x == goal_x and player_y == goal_y:
                score_text = font.render("You Win!", True, (0, 255, 255))
                screen.blit(score_text, (UI_X_OFFSET, GRID_HEIGHT + LIVES_HEIGHT))
                playing = False
            elif lives == 0:
                score_text = font.render("Game Over", True, (0, 255, 255))
                screen.blit(score_text, (UI_X_OFFSET, GRID_HEIGHT + LIVES_HEIGHT))
                playing = False

            # Update display
            pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
pygame.quit()
