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

ROBOT = '@'
BOX = 'O'
WALL = '#'
EMPTY = '.'

MOVES = {
    '^' : Coordinates(-1, 0),
    'v' : Coordinates(1, 0),
    '>' : Coordinates(0, 1),
    '<' : Coordinates(0, -1)
}

def parse_map_definition(map_definition):
    map = {}
    robot_position = None
    for x, line in enumerate(map_definition):
        for y, char in enumerate(line):
            map[Coordinates(x, y)] = char
            if char == ROBOT:
                robot_position = Coordinates(x, y)
    return map, len(map_definition), len(map_definition[0]), robot_position

def parse_instructions_definition(input_definition):
    instructions = ''
    for line in input_definition:
        instructions += line
    return instructions

def parse_input(input):
    cut_position = np.where(input == '')[0][0]
    map_definition = input[:cut_position]
    instructions_definition = input[cut_position + 1:]
    parsed_map, height, width, robot_position = parse_map_definition(map_definition)
    parsed_instructions = parse_instructions_definition(instructions_definition)
    return parsed_map, height, width, robot_position, parsed_instructions

def move_object(start_position, end_position, map):
    map[end_position] = map[start_position]
    map[start_position] = EMPTY
    return map

def execute_instruction(instruction, object_position, map, robot_position):
    target_position = object_position.add(MOVES[instruction])
    if map[target_position] == WALL:
        return False, map, robot_position
    if map[target_position] == BOX:
        moved, map, robot_position = execute_instruction(instruction, target_position, map, robot_position)
        if not moved:
            return False, map, robot_position
    if map[object_position] == ROBOT:
        robot_position = target_position
    map = move_object(object_position, target_position, map)
    return True, map, robot_position

def execute_instructions(instructions, robot_position, map):
    for instruction in instructions:
        _, map, robot_position = execute_instruction(instruction, robot_position, map, robot_position)
    return map

def total_GPS(map, height, width):
    total = 0
    for x in range(height):
        for y in range(width):
            if map[Coordinates(x, y)] == BOX:
                total += 100 * x + y
    return total

begin_time = datetime.datetime.now()

input_file = open("D:\\AdventOfCode\\15\\input.txt", "r")
input = np.array([line.strip() for line in input_file.readlines()])

warehouse_map, height, width, robot_position, instructions = parse_input(input)
end_map = execute_instructions(instructions, robot_position, warehouse_map)
result_part1 = total_GPS(end_map, height, width)
print(result_part1)

end_time = datetime.datetime.now()
print(f"Total execution time : {end_time - begin_time}")
