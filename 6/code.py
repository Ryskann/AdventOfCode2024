import numpy as np
from enum import Enum

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, coordinates):
        return Coordinates(self.x + coordinates.x, self.y + coordinates.y)
    
    def __eq__(self, coordinates):
        return self.x == coordinates.x and self.y == coordinates.y
    
    def __hash__(self):
        return hash(('x', self.x, 'y', self.y))
    
    def __str__(self):
        return f"x : {self.x}, y : {self.y}"

class Segment:
    def __init__(self, point_A, point_B):
        self.point_A = point_A
        self.point_B = point_B
        
    def __eq__(self, segment):
        return self.point_A == segment.point_A and self.point_B == segment.point_B
    
    def __hash__(self):
        return hash(('A', self.point_A, 'B', self.point_B))
    
    def __str__(self):
        return f"A : {self.point_A.x}_{self.point_A.y} ----- B : {self.point_B.x}_{self.point_B.y}"

class Directions(Enum):
    UP = Coordinates(-1,0)
    DOWN = Coordinates(1,0)
    RIGHT = Coordinates(0,1)
    LEFT = Coordinates(0,-1)

DIRECTIONS_ORDER = (Directions.UP, Directions.RIGHT, Directions.DOWN, Directions.LEFT)

GUARD_MARKER = '^'
PATH_MARKER = 'X'
OBSTRUCTION_MARKER = '#'

GUARD_DEFAULT_DIRECTION = Directions.UP

def get_guard_position(map):
    position = np.where(map == GUARD_MARKER)
    return Coordinates(position[0][0], position[1][0])

def value_to_obstruction_value(value):
    return value == OBSTRUCTION_MARKER

def get_obstruction_map(map):
    return get_guard_position(map), np.vectorize(value_to_obstruction_value)(map)

def get_map_slice(obstructions_map, start_position, guard_direction):
    match guard_direction:
        case Directions.UP:
            return obstructions_map[:start_position.x, start_position.y][::-1]
        case Directions.DOWN:
            return obstructions_map[start_position.x + 1:, start_position.y]
        case Directions.LEFT:
            return obstructions_map[start_position.x, :start_position.y][::-1]
        case Directions.RIGHT:
            return obstructions_map[start_position.x, start_position.y + 1:]

def new_guard_position(guard_position, guard_direction, path_lenght):
    match guard_direction:
        case Directions.UP:
            return Coordinates(guard_position.x - path_lenght, guard_position.y)
        case Directions.DOWN:
            return Coordinates(guard_position.x + path_lenght, guard_position.y)
        case Directions.LEFT:
            return Coordinates(guard_position.x, guard_position.y - path_lenght)
        case Directions.RIGHT:
            return Coordinates(guard_position.x, guard_position.y + path_lenght)

def trace_path(obstrictions_map, guard_position, guard_direction):
    map_slice = get_map_slice(obstrictions_map, guard_position, guard_direction)
    path_lenght = np.where(map_slice)[0]
    if(len(path_lenght) == 0):
        return len(map_slice), new_guard_position(guard_position, guard_direction, len(map_slice)), True
    else:
        return path_lenght[0], new_guard_position(guard_position, guard_direction, path_lenght[0]), False

def get_next_direction(current_direction):
    return DIRECTIONS_ORDER[(DIRECTIONS_ORDER.index(current_direction) + 1) % 4]

def get_positions(segment):
    positions = np.array([])
    for x in range(min(segment.point_A.x, segment.point_B.x), max(segment.point_A.x, segment.point_B.x) + 1):
        for y in range(min(segment.point_A.y, segment.point_B.y), max(segment.point_A.y, segment.point_B.y) + 1):
            positions = np.append(positions, [Coordinates(x, y)])
    return positions

def get_path(obstructions_map, guard_position, with_position_historic = True):
    guard_direction = GUARD_DEFAULT_DIRECTION
    is_end = False
    is_blocked = False
    segment_historic = np.array([])
    position_historic = np.array([guard_position])
    while(not is_end):
        old_guard_position = guard_position
        _, guard_position, is_end = trace_path(obstructions_map, guard_position, guard_direction)
        new_path_segment = Segment(old_guard_position, guard_position)
        if with_position_historic:
            for position in get_positions(new_path_segment):
                if not np.isin(position_historic, position).any():
                    position_historic = np.append(position_historic, [position])
        if not np.isin(segment_historic, new_path_segment).any():
            segment_historic = np.append(segment_historic, [new_path_segment])
        else:
            is_blocked = True
            break
        guard_direction = get_next_direction(guard_direction)
    return position_historic, position_historic.size, is_blocked

def get_all_ostruction_opportunities(obstructions_map, guard_position, historic_path):
    cpt = 0
    historic_path_lenght = len(historic_path)
    for i, historic_position in enumerate(historic_path):
        if not historic_position == guard_position:
            obstructions_map[historic_position.x, historic_position.y] = True
            _, _, is_blocked = get_path(obstructions_map, guard_position, False)
            if is_blocked:
                cpt += 1
            obstructions_map[historic_position.x, historic_position.y] = False
    return cpt

input_file = open("D:\\AdventOfCode\\6\\input.txt", "r")
map = np.array([list(line.strip()) for line in input_file.readlines()])

guard_position, obstructions_map = get_obstruction_map(map)
path_part1, result_part1, _ = get_path(obstructions_map, guard_position)
print(result_part1)

result_part2 = get_all_ostruction_opportunities(obstructions_map, guard_position, path_part1)
print(result_part2)
