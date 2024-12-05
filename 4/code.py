TARGET = 'XMAS'

UP = (1,0)
DOWN = (-1,0)
RIGHT = (0,1)
LEFT = (0,-1)
UP_RIGHT = (1,1)
UP_LEFT = (1,-1)
DOWN_RIGHT = (-1,1)
DOWN_LEFT = (-1,-1)
DIRECTIONS = (UP, DOWN, RIGHT, LEFT, UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT)

input_file = open("D:\\AdventOfCode\\4\\input.txt", "r")
input = [line.strip() for line in input_file.readlines()]

input_height = len(input)
input_width = len(input[0])

def add_coordinates(coordinates_1, coordinates_2):
    return tuple(x + y for x, y in zip(coordinates_1, coordinates_2))

def out_of_range(coordinates):
    return coordinates[0] < 0 or coordinates[0] >= input_height or coordinates[1] < 0 or coordinates[1] >= input_width

def look_for_rest_of_word_in_direction(target, coordinates, direction, position):
    if position == len(target):
        return True
    if out_of_range(coordinates):
        return False
    if input[coordinates[0]][coordinates[1]] == target[position]:
        return look_for_rest_of_word_in_direction(target, add_coordinates(coordinates, direction), direction, position + 1)
    
def look_for_word(coordinates):
    cpt = 0
    if (input[coordinates[0]][coordinates[1]] == TARGET[0]):
        for direction in DIRECTIONS:
            if look_for_rest_of_word_in_direction(TARGET, add_coordinates(coordinates, direction), direction, 1):
                cpt += 1
    return cpt

def scan_for_word():
    cpt = 0
    for x in range(input_height):
        for y in range(input_width):
            cpt += look_for_word((x,y))
    return cpt

result_part1 = scan_for_word()
print(result_part1)

#------------------------------------------------------------------------------------------------------------------

OPPOSITES = {
    UP : DOWN,
    DOWN : UP,
    RIGHT : LEFT,
    LEFT : RIGHT,
    UP_RIGHT : DOWN_LEFT,
    UP_LEFT : DOWN_RIGHT,
    DOWN_RIGHT : UP_LEFT,
    DOWN_LEFT : UP_RIGHT
}

SHAPE = (UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT)
SHAPE_TARGER = 'MAS'

shape_middle = SHAPE_TARGER[round(len(SHAPE_TARGER) / 2) - 1]

def shape_out_of_bounds(coordinates):
    for bound in SHAPE:
        if out_of_range(add_coordinates(coordinates, bound)):
            return True
    return False

def look_for_word_in_direction(coordinates, direction):
    cpt = 0
    if (input[coordinates[0]][coordinates[1]] == SHAPE_TARGER[0]):
        if look_for_rest_of_word_in_direction(SHAPE_TARGER, add_coordinates(coordinates, direction), direction, 1):
            cpt += 1
    return cpt

def is_shape(coordinates):
    cpt = 0
    for bound in SHAPE:
        cpt += look_for_word_in_direction(add_coordinates(coordinates, bound), OPPOSITES[bound])
    return cpt >= 2

def look_for_shape(coodinates):
    if shape_out_of_bounds(coodinates):
        return False
    return is_shape(coodinates)

def scan_for_shape():
    cpt = 0
    for x in range(input_height):
        for y in range(input_width):
            if look_for_shape((x,y)):
                cpt += 1
    return cpt

result_part2 = scan_for_shape()
print(result_part2)
