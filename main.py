import pygame
import sys
import asyncio

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([600, 500])
base_font = pygame.font.Font(None, 32)

# Function to initialize the grid with random values
def init_grid(rows, cols):
    grid = []
    for row in range(rows):
        grid.append([])
        for col in range(cols):
            grid[row].append(0)
    return grid

# Function to draw the grid lines
def draw_grid(grid, rows, cols):
    for row in range(rows):
        for col in range(cols):
            color = (255, 255, 255)
            if grid[row][col] == 1:
                color = (0, 0, 0)
            pygame.draw.rect(screen, color, (col * 10, row * 10, 10, 10), 0)

# Function to count live neighbors
def count_neighbors(grid, x, y, rows, cols):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            row = (x + i + rows) % rows
            col = (y + j + cols) % cols
            count += grid[row][col]
    count -= grid[x][y]
    return count

async def main():
    rows = 50
    cols = 60
    grid = init_grid(rows, cols)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid[y // 10][x // 10] = 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        next_grid = init_grid(rows, cols)

        for i in range(rows):
            for j in range(cols):
                neighbors = count_neighbors(grid, i, j, rows, cols)
                if grid[i][j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        next_grid[i][j] = 0
                    else:
                        next_grid[i][j] = 1
                else:
                    if neighbors == 3:
                        next_grid[i][j] = 1

        grid = next_grid
        screen.fill((0, 0, 0))
        draw_grid(grid, rows, cols)
        pygame.display.flip()
        clock.tick(10)
        await asyncio.sleep(0)

asyncio.run(main())

