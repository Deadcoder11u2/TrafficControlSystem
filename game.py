from random import random
from matplotlib.pyplot import bar
import pygame
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

# Initialize the game
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1245, 636))

maxCapBarrier = 10


class Signal:
    def __init__(self, isRed, road_no, coors, barrier):
        self.coors = coors
        self.isRed = isRed
        self.road_no = road_no
        self.wait_time = 0
        self.number_of_cars = 0
        self.barrier = barrier
        self.static_barrier = barrier
        self.cap_of_barrier = maxCapBarrier
        self.hori_delta = 0
        self.veri_delta = 0

    def reset(self):
        self.cap_of_barrier = maxCapBarrier

    def extend_barrier(self, h_del, v_del):
        self.barrier[0][0] += h_del
        self.barrier[1][0] += h_del
        self.barrier[0][1] += v_del
        self.barrier[1][1] += v_del


class Car:
    def __init__(self, coorX, coorY, direction, color, signal_no):
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

        # the color of the car
        self.color = color

        # in which signal the car is standing
        self.signal_no = signal_no

        # number of signal after the direction is changed
        self.next_signal_no = -1


def draw_lines(lines):
    for line in lines:
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 2)


class Padding:
    def __init__(self, fPoint, sPoint, padDist, directionList):
        self.fPoint = fPoint
        self.sPoint = sPoint
        self.padDist = padDist
        self.directionList = directionList
        # self.road_no = self.road_no

    def __str__(self) -> str:
        return str(self.fPoint) + str(self.sPoint) + str(self.padDist) + str(self.directionList)

    def draw_hori_padding(self):
        pygame.draw.line(screen, CYAN, self.fPoint, self.sPoint)
        nfPoint = (self.fPoint[0], self.fPoint[1]+self.padDist)
        nsPoint = (self.sPoint[0], self.sPoint[1] + self.padDist)
        pygame.draw.line(screen, CYAN, nfPoint, nsPoint)

    def draw_veri_padding(self):
        pygame.draw.line(screen, CYAN, self.fPoint, self.sPoint)
        nfPoint = (self.fPoint[0] + self.padDist, self.fPoint[1])
        nsPoint = (self.sPoint[0] + self.padDist, self.sPoint[1])
        pygame.draw.line(screen, CYAN, nfPoint, nsPoint)


pygame.display.set_caption("Traffic Control System")

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
        [(75, 170), (105, 170), (("R", (3, -1)), ("R", (3, -1))), 40],
        [(451, 170), (480, 170), (("R", (5, 0)), ("R", (5, 0))), 40],
        [(948, 170), (1005, 170), (("R", (0, -1)), ("D", (7, -1))), 40],
        [(273, 413), (310, 413), (("R", (14, -1)), ("R", (14, -1))), 21],
        [(948, 515), (1007, 515), (("R", (0, -1)), ("D", (0, -1))), 40],
        # upp paddings
        [(274, 260), (234, 260), (("L", (0, -1)), ("L", (0, -1))), -40],
        [(663, 260), (623, 260), (("L", (11, -1)), ("L", (11, -1))), -40],
        [(948, 260), (885, 260), (("L", (9, -1)), ("U", (0, -1))), -40],
        [(663, 468), (628, 468), (("L", (17, -1)), ("U", (10, -1))), -25],
        [(130, 468), (94, 468), (("L", (0, -1)), ("L", (0, -1))), -25]
    ]

    veri_paddings = [
        # Right paddings
        [(44, 214), (44, 170), (("U", (0, -1)), ("R", (3, -1))), 20],
        [(417, 214), (417, 170), (("U", (0, -1)), ("R", (5, 0))), 20],
        [(894, 214), (894, 170), (("U", (0, -1)), ("R", (0, -1))), 40],
        [(238, 438), (238, 410), (("U", (12, -1)), ("U", (12, -1))), 20],
        [(627, 439), (627, 411), (("U", (10, -1)), ("U", (10, -1))), 20],
        # Left paddings
        [(307, 264), (307, 217), (("D", (16, -1)), ("L", (0, -1))), -20],
        [(696, 264), (696, 217), (("D", (0, -1)), ("L", (11, -1))), -20],
        [(1001, 264), (1001, 217), (("D", (7, -1)), ("L", (9, -1))), -40],
        [(1001, 578), (1001, 550), (("D", (0, -1)), ("D", (0, -1))), -20],
        [(162, 471), (162, 440), (("D", (0, -1)), ("L", (0, -1))), -20]
    ]
    for line in hori_padding:
        horizontal_paddings.append(
            Padding(fPoint=line[0], sPoint=line[1], padDist=line[3], directionList=line[2]))
    for line in veri_paddings:
        vertical_paddings.append(
            Padding(fPoint=line[0], sPoint=line[1], padDist=line[3], directionList=line[2]))


signals = []


def initialize_signals():
    coordinates = [
        [(36, 192, (-10, 0)), ((30, 214), (30, 170))],
        [(92, 154, (0, -10)), ((74, 160), (108, 160))],
        [(395, 193, (-10, 0)), ((409, 216), (409, 169))],
        [(467, 146, (0, -10)), ((451, 163), (480, 163))],
        [(865, 193, (-10, 0)), ((889, 215), (889, 169)),
         (1020, 230, (10, 0)), ((1009, 216), (1009, 264))],
        [(977, 156, (0, 10)), ((894, 272), (947, 272)),
         (924, 272, (0, -10)), ((949, 162), (999, 162))],
        [(977, 480, (0, -10)), ((950, 500), (999, 500))],
        [(1030, 568, (10, 0)), ((1008, 548), (1008, 577))],
        [(715, 236, (10, 0)), ((699, 265), (699, 237))],
        [(648, 280, (0, 10)), ((627, 272), (667, 272))],
        [(332, 236, (0, 10)), ((314, 261), (213, 216))],
        [(254, 288, (-10, 0)), ((237, 269), (271, 269))],
        [(645, 500, (0, 10)), ((628, 480), (663, 480))],
        [(608, 425, (-10, 0)), ((619, 410), (619, 438))],
        [(209, 425, (-10, 0)), ((232, 408), (232, 438))],
        [(293, 387, (0, -10)), ((273, 396), (306, 296))],
        [(189, 457, (10, 0)), ((171, 440), (171, 471))],
        [(115, 497, (0, 10)), ((97, 476), (132, 476))]
    ]
    cnt = 0
    signals.append(Signal(isRed=False, road_no=0, coors=(
        (-5, -5, (0, 0)), (-5, -5), (0, 0)), barrier=(-10, -10)))
    for cnt in range(1, len(coordinates)+1):
        temp = coordinates[cnt-1]
        if cnt == 5:
            signals.append(Signal(isRed=cnt % 2 == 0, road_no=5, coors=(
                coordinates[cnt-1][0], coordinates[cnt-1][2]), barrier=(coordinates[cnt-1][1], coordinates[cnt-1][3])))
            continue
        if cnt == 6:
            signals.append(Signal(isRed=cnt % 2 == 0, road_no=6, coors=(
                coordinates[cnt-1][0], coordinates[cnt-1][2]), barrier=(coordinates[cnt-1][1], coordinates[cnt-1][3])))
            continue
        signals.append(Signal(isRed=cnt % 2 == 0, road_no=cnt, coors=(
            (temp[0]), (temp[0][0], temp[0][1], temp[0][2])), barrier=temp[1]))


def render_signals():
    for sig in signals:
        if sig == "Srikanth":
            continue
        for i in sig.coors:
            if sig.isRed:
                pygame.draw.circle(screen, RED, (i[0], i[1]), 20, 30)
            else:
                pygame.draw.circle(screen, GREEN, (i[0], i[1]), 20, 30)


def check_point_on_hor_line(line, point):
    x1 = min(line[0][0], line[1][0])
    x2 = max(line[0][0], line[1][0])
    if point[0] >= x1 and point[0] <= x2 and point[1] == line[0][1]:
        return True
    return False


def check_point_on_ver_line(line, point):
    y1 = min(line[0][1], line[1][1])
    y2 = max(line[0][1], line[1][1])
    if point[1] >= y1 and point[1] <= y2 and point[0] == line[0][0]:
        return True
    return False


def render_existing_cars():
    global placed_cars
    new_placed = []
    for car in placed_cars:
        barrier = signals[car.signal_no[0]].barrier
        x = car.coorX
        y = car.coorY
        pt1 = ()
        pt2 = ()
        displacement = ()
        if car.signal_no[0] == 6 or car.signal_no[0] == 5:
            pt1 = barrier[car.signal_no[1]][0]
            pt2 = barrier[car.signal_no[1]][1]
        else:
            pt1 = barrier[0]
            pt2 = barrier[1]
            print(signals[car.signal_no[0]].coors)
            displacement = signals[car.signal_no[0]].coors[0][2]

        crossing = True
        if signals[car.signal_no[0]].isRed:
            if car.direction == 'D' or car.direction == 'U':
                crossing &= check_point_on_hor_line((pt1, pt2), (x, y))
            else:
                crossing &= check_point_on_ver_line((pt1, pt2), (x, y))

        crossing &= signals[car.signal_no[0]].isRed

        if not crossing:
            if car.direction == 'U' or car.direction == 'D':
                for padding in horizontal_paddings:
                    if check_point_on_hor_line((padding.fPoint, padding.sPoint), (car.coorX, car.coorY)):
                        car.toChange = True
                        tt = random.choice(padding.directionList)
                        car.nextDirection = tt[0]
                        car.next_signal_no = tt[1]
                        car.nextChangeDistance = randint(
                            3, abs(padding.padDist))
            else:
                for padding in vertical_paddings:
                    if check_point_on_ver_line((padding.fPoint, padding.sPoint), (car.coorX, car.coorY)):
                        car.toChange = True
                        tt = random.choice(padding.directionList)
                        car.nextDirection = tt[0]
                        car.next_signal_no = tt[1]
                        car.nextChangeDistance = randint(
                            3, abs(padding.padDist))
        if car.toChange:
            if car.nextChangeDistance == 0:
                car.direction = car.nextDirection
                car.signal_no = car.next_signal_no
                car.nextDirection = "?"
                car.nextChangeDistance = 0
                car.toChange = False
                car.next_signal_no = 0
            else:
                car.nextChangeDistance -= speed

        if not crossing:
            if car.direction == 'R':
                x += speed
            elif car.direction == 'L':
                x -= speed
            elif car.direction == 'D':
                y += speed
            else:
                y -= speed
        else:
            signals[car.signal_no[0]].cap_of_barrier -= 1
            # if signals[car.signal_no[0]].cap_of_barrier == 0:
            #     signals[car.signal_no[0]].reset()
            #     signals[car.signal_no[0]].extend_barrier(displacement[0], displacement[1])

        car.coorX, car.coorY = x, y
        if x > 1245 or x < 0 or y > 636 or y < 0:
            continue
        new_placed.append(car)
        pygame.draw.circle(screen, car.color, (x, y), 5, 5)
    placed_cars = new_placed
    # print()


valid_points_to_generate = [
    # points where cars can generate added padding
    [(0, 171), (0, 210), "R", (1, -1)],
    [(78, 2), (103, 2), "D", (2, -1)],
    [(2, 412), (2, 435), "R", (15, -1)],
    [(102, 625), (125, 625), "U", (18, -1)],
    [(456, 41), (477, 41), "D", (4, -1)],
    [(955, 41), (996, 41), "D", (6, 1)],
    [(1231, 221), (1231, 256), "L", (5, 1)],
    [(1234, 550), (1233, 573), "L", (8, -1)],
    [(633, 625), (657, 628), "U", (13, -1)],
    [(895, 630), (940, 630), "U", (18, -1)]
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
    placed_cars.append(
        Car(coorX=x, coorY=y, direction=line[2], color=BLUE, signal_no=line[3]))


def draw_valid_points():
    for i in valid_points_to_generate:
        pygame.draw.line(screen, CYAN, i[0], i[1])


def draw_road():
    road = [
        [(0, 170), (42, 170)],
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
    for line in road:
        pygame.draw.line(screen, LIME, line[0], line[1])


running = True
image = pygame.image.load(r'mywork/road.png')
car = pygame.image.load(r'car_1.png')
start_time = time()

initialize_padding()
initialize_signals()


def flip_signal():
    for idx in range(1, len(signals)):
        signals[idx].isRed ^= True


timer = 1

while running:
    screen.blit(image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    render_existing_cars()
    render_signals()
    for padding in vertical_paddings:
        padding.draw_veri_padding()
    now_time = time()
    if(now_time - start_time > 1):
        rand_car()
        rand_car()
        rand_car()
        rand_car()
        rand_car()
        rand_car()
        timer += 1
        start_time = now_time
    if timer % 10 == 0:
        flip_signal()
        timer += 1
    pygame.display.update()
