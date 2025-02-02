import numpy as np
import math
import datetime

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, coordinates):
        return Coordinates(self.x + coordinates.x, self.y + coordinates.y)
    
    def minus(self, coordinates):
        return Coordinates(self.x - coordinates.x, self.y - coordinates.y)
    
    def multiply(self, mult):
        return Coordinates(self.x * mult, self.y * mult)
    
    def __eq__(self, coordinates):
        if type(coordinates) != Coordinates:
            return False
        return self.x == coordinates.x and self.y == coordinates.y
    
    def __hash__(self):
        return hash(('x', self.x, 'y', self.y))
    
    def __str__(self):
        return f"x : {self.x}, y : {self.y}"

class Robot:
    def __init__(self, limits, start_position, velocity):
        self.limits = limits
        self.position = start_position
        self.velocity = velocity
    
    def emulate_a_second(self):
        self.position.x = (self.position.x + self.velocity.x) % self.limits.x
        self.position.y = (self.position.y + self.velocity.y) % self.limits.y
    
    def emulate_seconds(self, seconds):
        for _ in range(seconds):
            self.emulate_a_second()
    
    def get_position(self):
        return self.position

def create_robots(input, max_x, max_y):
    robots = np.array([])
    for line in input:
        p_str, v_str = line.split()
        px, py = map(int, p_str.split('=')[1].split(','))
        vx, vy = map(int, v_str.split('=')[1].split(','))
        new_robot = Robot(
            Coordinates(max_x, max_y),
            Coordinates(px, py),
            Coordinates(vx, vy)
        )
        robots = np.append(robots, [new_robot])
    return robots

def emulate_robots(robots, seconds):
    for robot in robots:
        robot.emulate_seconds(seconds)

def get_safety_factor(robots, max_x, max_y):
    q1, q2, q3, q4 = 0, 0, 0, 0
    for robot in robots:
        if robot.position.x <= math.floor(max_x / 2) - 1:
            if robot.position.y <= math.floor(max_y / 2) - 1:
                q1 += 1
            if robot.position.y >= math.ceil(max_y / 2):
                q2 += 1
        if robot.position.x >= math.ceil(max_x / 2):
            if robot.position.y <= math.floor(max_y / 2) - 1:
                q3 += 1
            if robot.position.y >= math.ceil(max_y / 2):
                q4 += 1
    return q1 * q2 * q3 * q4

def print_robots(robots, max_x, max_y):
    picture = []
    for _ in range(max_x):
        picture_line = []
        for _ in range(max_y):
            picture_line.append('.')
        picture.append(picture_line)
    for x in range(max_x):
        for y in range(max_y):
            for robot in robots:
                if robot.position == Coordinates(x, y):
                    picture[x][y] = 'X'
    printable_picture = ""
    for x in range(max_x):
        for y in range(max_y):
            printable_picture += picture[x][y]
        printable_picture += '\n'
    print(printable_picture)

def emulate_and_print(robots, seconds , max_x, max_y, each = 1):
    for second in range(seconds):
        for robot in robots:
            robot.emulate_seconds(1)
        if second % each == 0:
            print(f"Second : {second} for picture bellow")
            print_robots(robots, max_x, max_y)
      

WIDTH = 101 #101 #11
HEIGHT = 103 #103 #7
TIME = 100

begin_time = datetime.datetime.now()

input_file = open("D:\\AdventOfCode\\14\\input.txt", "r")
input = np.array([line.strip() for line in input_file.readlines()])

robots = create_robots(input, WIDTH, HEIGHT)
emulate_robots(robots, 100)
result_part1 = get_safety_factor(robots, WIDTH, HEIGHT)
print(result_part1)

picture_robots = create_robots(input, WIDTH, HEIGHT)
emulate_and_print(robots, 100, WIDTH, HEIGHT, 1)

end_time = datetime.datetime.now()
print(f"Total execution time : {end_time - begin_time}")