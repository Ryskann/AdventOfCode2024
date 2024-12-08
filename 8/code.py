import numpy as np

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
    
    def get_diff(self):
        return Coordinates(self.point_B.x - self.point_A.x, self.point_B.y - self.point_A.y)

EMPTY_MARKER = '.'

def get_antennas(map) -> dict:
    antennas = {}
    for x, line in enumerate(map):
        for y, char in enumerate(line):
            if not char == EMPTY_MARKER:
                if not char in antennas.keys():
                    antennas[char] = np.array([Coordinates(x, y)])
                else:
                    antennas[char] = np.append(antennas[char], np.array([Coordinates(x, y)]))
    return antennas

def out_of_bounds(coordinates, bounds) -> bool:
    return coordinates.x < 0 or coordinates.x >= bounds.x or coordinates.y < 0 or coordinates.y >= bounds.y

def get_antinodes(antennas, max_range = 1) -> set:
    bounds = Coordinates(len(map), len(map[0]))
    antennas = get_antennas(map)
    antinodes = np.array([])
    for antenna_frequency in antennas.keys():
        for antenna_1 in antennas[antenna_frequency]:
            for antenna_2 in antennas[antenna_frequency]:
                if not antenna_1 == antenna_2:
                    position_diff = Segment(antenna_1, antenna_2).get_diff()
                    start_position = antenna_2 if max_range == 1 else antenna_1
                    range_form_antenna = 1
                    while(range_form_antenna <= max_range):
                        potential_antinode = start_position.add(position_diff)
                        start_position = potential_antinode
                        if not out_of_bounds(potential_antinode, bounds):
                            antinodes = np.append(antinodes, np.array([potential_antinode]))
                            range_form_antenna += 1
                        else:
                            break
    return np.array(list(set(antinodes)))
            
        
input_file = open("D:\\AdventOfCode\\8\\input.txt", "r")
map = np.array([np.array(list(line.strip())) for line in input_file.readlines()])

antinodes = get_antinodes(map)

result_part1 = len(antinodes)
print(result_part1)

antinodes_distant = get_antinodes(map, 100)
result_part2 = len(antinodes_distant)
print(result_part2)
