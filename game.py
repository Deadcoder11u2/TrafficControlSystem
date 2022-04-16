import pygame 
from pygame import gfxdraw

#Colors 
RED = (255, 0, 0)


# Initialize the game
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")

#player
car = pygame.image.load('car_1.png')
carX = 300
carY = 300

def carPlace():
    screen.blit(car, (carX, carY))

def draw_circle(x, y, color):
    pygame.draw.circle(screen, color, (x, y), 5, 5)

def draw_road():
    road = [
        [(0, 150), (150, 150)],
        [(0, 250), (250, 250)],
        [(0, 400), (250, 400)],
        [(0, 500), (250, 500)],
        [(250, 250), (250, 400)],
        [(150, 0), (150, 150)],
        [(250, 0), (250, 150)]
    ]
    for line in road:
        pygame.draw.line(screen, RED, line[0], line[1])

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    # draw_circle(0, 0, (255, 0, 0))
    draw_road()
    pygame.display.update()