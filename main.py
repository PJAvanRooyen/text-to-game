import pygame 

# define the window size 
window_width = 800
window_height = 600

# initialize pygame 
pygame.init()
pygame.mixer.init()

# create a surface and define the window 
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Conway's Game of Life")

# create a font 
font = pygame.font.Font('freesansbold.ttf', 24)

# create a color 
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# create the game loop 
while True:
    # get the events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # create the surface 
    surface = pygame.Surface((window_width, window_height))
    surface.fill(black)
    
    # draw the grid 
    pygame.draw.line(surface, white, [0, 0], [window_width, window_height], 5)
    pygame.draw.line(surface, white, [0, 0], [0, window_height], 5)
    pygame.draw.line(surface, white, [window_width, 0], [window_width, window_height], 5)
    pygame.draw.line(surface, white, [window_width, window_height], [0, 0], 5)
    
    # create a surface to display the text 
    text_surface = font.render('Conway\'s Game of Life', False, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (window_width // 2, window_height // 2)
    surface.blit(text_surface, text_rect)
    
    # display the surface 
    pygame.display.flip()