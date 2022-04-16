from random import Random
from matplotlib.pyplot import draw
import pygame 
from pygame import gfxdraw
from random import randint
from time import  time

# class Car:
#     def __init__(x_corr, y_coor):
#         self.x_coor = x_coor
#         self.y_coor = y_coor
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

placed_cars = []

def render_existing_cars():
    for coor in placed_cars:
        x = coor[0][0]
        y = coor[0][1]
        if coor[1] == 'R':
            x += 1
        elif coor[1] == 'L':
            x -= 1
        elif coor[1] == 'D':
            y += 1
        else:
            y -= 1
        coor[0] = [x, y]
        pygame.draw.circle(screen, BLUE, (x, y), 5, 5)

valid_points_to_generate = [
    [(0, 170), (0, 215), "R"],           # Vertical line
    [(0,215) , (0,260),"L"],
    [(0, 410), (0, 440), "V"],           # Vertical line
    [(0, 440), (0, 470), "V"],
    [(100, 600), (130, 600), "H"],       # Horizontal line
    [(130, 600), (160, 600), "H"],
    [(630, 600), (665, 600), "H"],       # Horizontal line
    [(665, 600), (700, 600), "H"],
    [(417, 0), (448, 0), "H"],           # Horizontal line
    [(448, 0), (480, 0), "H"],
    [(1242, 515), (1242, 544), "V"],     # Vertical line
    [(1242, 544), (1242, 574), "V"],
]

def rand_car():
    idx = randint(0, len(valid_points_to_generate) - 1)
    line = valid_points_to_generate[idx]
    x, y = -1, -1
    if line[2] == "V":
        x = line[0][0]
        y = randint(line[0][1], line[1][1])
    else:
        y = line[0][1]
        x = randint(line[0][0], line[1][0])
    print(line, x, y)
    placed_cars.append([[x, y], "D"])



def draw_valid_points():
    for i in valid_points_to_generate:
        pygame.draw.line(screen, CYAN, i[0], i[1])

# Function to draw all the roads
def draw_road():
    road = [
        [(0, 170), (42, 170), "H"],
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
car = pygame.image.load(r'car_1.png')
start_time = time()

while running:
    screen.blit(image,(0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    render_existing_cars()
    draw_road()
    now_time = time()
    screen.blit(car, (0, 200))
    # rand_car()
    if(now_time - start_time > 4):
        rand_car()
        print("PRINTING")
        start_time = now_time
    pygame.display.update()