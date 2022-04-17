from fileinput import hook_encoded
from random import Random, random
from matplotlib.pyplot import draw
import pygame
from pygame import gfxdraw
from time import time
from random import *
import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER = (192, 192, 192)
LIME = (124, 255, 0)


class Car:
    def __init__(self, coorX, coorY, direction):
        # Current coordinates of the car
        self.coorX = coorX
        self.coorY = coorY

        # the direction in which the car is moving
        self.direction = direction

        # flag to stop the car when the signal is red
        self.stop = False

        # whether the car has passed the padding region
        self.toChange = False

        # if it has crossed the padding region then in which direction it should move
        self.nextDirection = "?"

        # if it has crossed the padding region then after what distance the direction should change
        self.nextChangeDistance = 0


def draw_lines(lines):
    for line in lines:
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 2)


# Initialize the game
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1245, 636))


class Padding:
    def __init__(self, fPoint, sPoint, padDist, directionList):
        self.fPoint = fPoint
        self.sPoint = sPoint
        self.padDist = padDist
        self.directionList = directionList

    def __str__(self) -> str:
        return str(self.fPoint) + str(self.sPoint) + str(self.padDist) + str(self.directionList)

    def draw_padding(self):
        pygame.draw.line(screen, CYAN, self.fPoint, self.sPoint)
        nfPoint = (self.fPoint[0], self.fPoint[1]+self.padDist)
        nsPoint = (self.sPoint[0], self.sPoint[1] + self.padDist)
        pygame.draw.line(screen, CYAN, nfPoint, nsPoint)


pygame.display.set_caption("Space Invaders")

placed_cars = []

# what should be the speed of the cars
speed = 1

horizontal_paddings = []
vertical_paddings = []

def initialize_padding():
    global horizontal_paddings, vertical_paddings
    # padding lines
    # horizontal padding
    hori_padding = [
        # down paddings
        [(75, 170), (105, 170), ("R"), 40],
        [(451, 170), (480, 170), ("R"), 40],
        [(948, 170), (1005, 170), ("R", "D"), 40],
        [(273, 413), (310, 413), ("R"), 21],
        [(948, 515), (1007, 515), ("R", "D"), 40],
        # upp paddings
        [(274, 260), (234, 260), ("L"), -40],
        [(663, 260), (623, 260), "L", -40],
        [(948, 260), (885, 260), ("L", "U"), -40],
        [(663, 468), (628, 468), ("L", "U"), -25],
        [(130, 468), (94, 468), ("L"), -25]
    ]

    veri_paddings = [
        # Right paddings
        [(44, 214), (44, 170), ("U", "R"), 20],
        [(417, 214), (417, 170), ("U", "R"), 20],
        [(894, 214), (894, 170), ("U", "R"), 40],
        [(238, 438), (238, 410), ("U"), 20],
        [(627, 439), (627, 411), ("U"), 20],
        # Left paddings
        [(307, 264), (307, 217), ("D", "L"), -20],
        [(696, 264), (696, 217), ("D", "L"), -20],
        [(1001, 264), (1001, 217), ("D", "L"), -40],
        [(1001, 578), (1001, 550), ("D"), -20],
        [(162, 471), (162, 440), ("D", "L"), -20]
    ]
    for line in hori_padding:
        horizontal_paddings.append(Padding(fPoint=line[0], sPoint=line[1], padDist=line[3], directionList=line[2]))
    for line in veri_paddings:
        vertical_paddings.append(Padding(fPoint=line[0], sPoint=line[1], padDist=line[3], directionList=line[2]))

def check_point_on_hor_line(line, point):
    x1 = min(line[0][0], line[1][0])
    x2 = max(line[0][0], line[1][0])
    if point[0] >= x1 and point[0] <= x2 and point[1] == line[0][1]:
        return True
    return False

def check_point_on_ver_line(line, point):
    y1 = min(line[0][1], line[1][1]);
    y2 = max(line[0][1], line[1][1])
    if point[1] >= y1 and point[1] <= y2 and point[0] == line[0][0]:
        return True
    return False

def render_existing_cars():
    global placed_cars
    new_placed = []
    for car in placed_cars:
        if car.direction == 'U' or car.direction == 'D':
            for padding in horizontal_paddings:
                if check_point_on_hor_line((padding.fPoint, padding.sPoint), (car.coorX, car.coorY)):
                    car.toChange = True
                    car.nextDirection = random.choice(padding.directionList)
                    car.nextChangeDistance = randint(3, abs(padding.padDist))
        else:
            for padding in vertical_paddings:
                if check_point_on_ver_line((padding.fPoint, padding.sPoint), (car.coorX, car.coorY)):
                    car.toChange = True
                    car.nextDirection = random.choice(padding.directionList)
                    car.nextChangeDistance = randint(3, abs(padding.padDist))
        x = car.coorX
        y = car.coorY
        if car.toChange:
            if car.nextChangeDistance == 0:
                car.direction =  car.nextDirection
                car.nextDirection = "?"
                car.nextChangeDistance = 0
                car.toChange = False
            else:
                car.nextChangeDistance -= speed
        if car.direction == 'R':
            x += speed
        elif car.direction == 'L':
            x -= speed
        elif car.direction == 'D':
            y += speed
        else:
            y -= speed
        car.coorX, car.coorY = x, y
        if x > 1245 or x < 0 or y > 636 or y < 0:
            continue
        new_placed.append(car)
        pygame.draw.circle(screen, BLUE, (x, y), 5, 5)
    placed_cars = new_placed


valid_points_to_generate = [
    # points where cars can generate added padding
    [(0, 174), (0, 210), "R"],
    [(78, 2), (103, 2), "D"],
    [(2, 412), (2, 435), "R"],
    [(102, 625), (125, 625), "U"],
    [(456, 41), (477, 41), "D"],
    [(955, 41), (996, 41), "D"],
    [(1231, 221), (1231, 256), "L"],
    [(1234, 550), (1233, 573), "L"],
    [(950, 624), (997, 625), "U"],
    [(633, 625), (657, 628), "U"]
    # [(948, 29), (1002, 29), ("D")]
]


def rand_car():
    idx = randint(0, len(valid_points_to_generate) - 1)
    line = valid_points_to_generate[idx]
    x, y = -1, -1
    if line[2] == "V":
        x = line[0][0]
        y = randint(min(line[0][1], line[1][1]), max(line[0][1], line[1][1]))
    else:
        y = line[0][1]
        x = randint(min(line[0][0], line[1][0]), max(line[0][0], line[1][0]))
    print(line, x, y)
    placed_cars.append(Car(coorX=x, coorY=y, direction=line[2]))


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
        [(106, 170), (106, 0)],
        [(106, 170), (415, 170)],
        [(415, 0), (415, 170)],
        [(480, 0), (480, 170)],
        [(480, 170), (890, 170)],
        [(890, 170), (890, 0)],
        [(1000, 170), (1000, 0)],
        [(1000, 170), (1240, 170)],
        [(1000, 260), (1240, 260)],
        [(1000, 520), (1240, 520)],
        [(1000, 580), (1240, 580)],
        [(1000, 580), (1000, 630)],
        [(1000, 260), (1000, 520)],
        [(700, 260), (890, 260)],
        [(890, 260), (890, 630)],
        [(700, 260), (700, 630)],
        [(625, 260), (625, 410)],
        [(625, 410), (303, 410)],
        [(303, 410), (303, 260)],
        [(0, 410), (237, 410)],
        [(237, 410), (237, 260)],
        [(237, 260), (0, 260)],
        [(307, 260), (625, 260)],
        [(0, 470), (100, 470)],
        [(100, 470), (100, 630)],
        [(160, 470), (160, 630)],
        [(160, 470), (630, 470)],
        [(630, 470), (630, 630)]
    ]


running = True
image = pygame.image.load(r'road.png')
car = pygame.image.load(r'car_1.png')
start_time = time()

initialize_padding()

    
for temp in horizontal_paddings:
    print(temp)
while running:
    screen.blit(image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    for i in horizontal_paddings:
        i.draw_padding()
    # draw_lines(hori_padding)
    render_existing_cars()
    draw_road()
    now_time = time()
    if(now_time - start_time > 1):
        rand_car()
        start_time = now_time
    pygame.display.update()
