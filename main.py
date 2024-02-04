import pygame
import asyncio
import random

# define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Conway's Game of Life")

# create a grid of squares
grid = [[False for _ in range(500)] for _ in range(500)]

# create a font for displaying numbers
font = pygame.font.Font('freesansbold.ttf', 30)

# create a function to display the grid
def draw_grid():
    for row in range(500):
        for col in range(500):
            if grid[row][col]:
                pygame.draw.rect(screen, GREEN, (col*50, row*50, 50, 50))
            else:
                pygame.draw.rect(screen, BLACK, (col*50, row*50, 50, 50))
    pygame.display.flip()

# create a function to update the grid
def update_grid(neighbors):
    for row in range(500):
        for col in range(500):
            # get the number of neighbors
            num_neighbors = sum([grid[r][c] for r, c in neighbors if grid[r][c]])
            # update the grid
            grid[row][col] = num_neighbors == 3 or (num_neighbors == 2 and grid[row][col])

# create a function to display the neighbors
def draw_neighbors(row, col):
    neighbors = [(r, c) for r, c in [(row-1, col), (row-1, col-1), (row, col-1), (row+1, col-1), (row+1, col), (row+1, col+1), (row, col+1), (row-1, col+1)]]
    for neighbor in neighbors:
        if neighbor in grid:
            update_grid(neighbors)
        else:
            grid.append(neighbor)
            update_grid(neighbors)
    draw_grid()

# create a function to handle the events
def event_handler(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
        elif event.key == pygame.K_r:
            draw_grid()
        elif event.key == pygame.K_SPACE:
            draw_neighbors(50, 50)

# create the main function
async def main():
    while True:
        # handle events
        for event in pygame.event.get():
            event_handler(event)
        # update the grid
        await asyncio.sleep(1)

# run the game
asyncio.run(main())