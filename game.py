import pygame 

# Initialize the game
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")

#player
car = pygame.image.load('car_4.png')
carX = 370
carY = 480

def carPlace():
    screen.blit(car, (carX, carY))

running = True 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    carPlace()
    pygame.display.update()