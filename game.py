import pygame 
from pygame import gfxdraw

#Colors 
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER = (192, 192, 192)
LIME = (124, 255, 0)

# Initialize the game
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1245, 636))

pygame.display.set_caption("Space Invaders")

# Function to draw a circle
def draw_circle(x, y, color):
    pygame.draw.circle(screen, color, (x, y), 5, 5)

valid_points_to_generate = [
    [(0, 170), (0, 260)],
    [(0, 410), (0, 470)],
    [(100, 600), (160, 600)],
    [(630, 600), (700, 600)],
    [(417, 0), (480, 0)],
    [(1240, 515), (1242, 574)],
]

def draw_valid_points():
    for i in valid_points_to_generate:
        pygame.draw.line(screen, CYAN, i[0], i[1])

# Function to draw all the roads
def draw_road():
    road = [
        [(0, 170), (42, 170)],
        [(42, 0), (42, 170)],
        [(0, 260), (240, 260)],
        [(0, 410), (240, 410)],
        [(106,170),(106,0)],
        [(106,170),(415,170)],
        [(415,0) , (415,170)],
        [(480,0), (480,170)],
        [(480,170), (890,170)],
        [(890,170), (890,0)],
        [(1000,170), (1000,0)],
        [(1000,170) , (1240,170)],
        [(1000,260), (1240,260)],
        [(1000,520), (1240,520)],
        [(1000,580) , (1240,580)],
        [(1000,580) , (1000,630)],
        [(1000,260) , (1000,520)],
        [(700,260) , (890,260)],
        [(890,260), (890,630)],
        [(700,260), (700,630)],
        [(625,260) , (625,410)],
        [(625,410) , (303,410)],
        [(303,410) , (303,260)],
        [(0,410) , (237,410)],
        [(237,410) , (237,260)],
        [(237,260) , (0,260)],
        [(307,260) , (625,260)],
        [(0,470) , (100,470)],
        [(100,470) , (100,630)],
        [(160,470), (160,630)],
        [(160,470), (630,470)],
        [(630,470) , (630,630)]
    ]
    for line in road:
        pygame.draw.line(screen, RED, line[0], line[1])

running = True 
image = pygame.image.load(r'road.png')
while running:
    screen.blit(image,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    draw_road()
    draw_valid_points()
    pygame.display.update()