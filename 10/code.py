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
    
    def out_of_bounds(self, bounds) -> bool:
        return self.x < 0 or self.x >= bounds.x or self.y < 0 or self.y >= bounds.y

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
    
    def get_diff(self):
        return Coordinates(self.point_B.x - self.point_A.x, self.point_B.y - self.point_A.y)

class Directions(Enum):
    UP = Coordinates(-1,0)
    DOWN = Coordinates(1,0)
    RIGHT = Coordinates(0,1)
    LEFT = Coordinates(0,-1)

def look_for_rest_of_trail(current_coord, map, bounds):
    current_value = map[current_coord.x][current_coord.y]
    if current_value == '9':
        return 1, [current_coord]
    value = 0
    reachable_coords = []
    for dir in Directions:
        potential_next = current_coord.add(dir.value)
        if not potential_next.out_of_bounds(bounds):
            if map[potential_next.x][potential_next.y] == str(int(current_value) + 1):
                added_value, nines_coords = look_for_rest_of_trail(potential_next, map, bounds)
                value += added_value
                reachable_coords = np.append(reachable_coords, nines_coords)
    return value, reachable_coords

def get_trailhead_value(coord_trailhead, map, bounds):
    number_of_trails, reachable_nines = look_for_rest_of_trail(coord_trailhead, map, bounds)
    return number_of_trails, len(set(reachable_nines))

def get_total_trailheads_value(map, bounds):
    number_of_trails = 0
    reachable_nines = 0
    for x in range(bounds.x):
        for y in range(bounds.y):
            if map[x][y] == str(0):
                added_value, reachable_coords = get_trailhead_value(Coordinates(x, y), map, bounds)
                number_of_trails += added_value
                reachable_nines += reachable_coords
    return number_of_trails, reachable_nines

input_file = open("D:\\AdventOfCode\\10\\input.txt", "r")
map = np.array([line.strip() for line in input_file.readlines()])

bounds = Coordinates(len(map), len(map[0]))


total_trailheads_value = get_total_trailheads_value(map, bounds)

result_part1 = total_trailheads_value[1]
print(result_part1)

result_part2 = total_trailheads_value[0]
print(result_part2)
