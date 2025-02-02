import numpy as np
import collections
import datetime

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def add(self, coordinates):
        return Coordinates(self.x + coordinates.x, self.y + coordinates.y)
    
    def __eq__(self, coordinates):
        if type(coordinates) != Coordinates:
            return False
        return self.x == coordinates.x and self.y == coordinates.y
    
    def __hash__(self):
        return hash(('x', self.x, 'y', self.y))
    
    def __str__(self):
        return f"x : {self.x}, y : {self.y}"
    
    def out_of_bounds(self, bounds) -> bool:
        return self.x < 0 or self.x >= bounds.x or self.y < 0 or self.y >= bounds.y
    
    def near(self, coordinates, range, diag = True) -> bool:
        x_dif = self.x - coordinates.x
        y_dif = self.y - coordinates.y
        if diag :
            return abs(x_dif) <= range and abs(y_dif) <= range
        return (abs(x_dif) <= range and y_dif == 0) or (abs(y_dif) <= range and x_dif == 0)

class Segment:
    def __init__(self, point_A, point_B):
        self.point_A = point_A
        self.point_B = point_B
        
    def __eq__(self, segment):
        if (type(segment) != Segment):
            return False
        return (self.point_A == segment.point_A and self.point_B == segment.point_B) or (self.point_A == segment.point_B and self.point_B == segment.point_A)
    
    def __hash__(self):
        return hash(('A', self.point_A, 'B', self.point_B))
    
    def __str__(self):
        return f"A : {self.point_A.x}_{self.point_A.y} ----- B : {self.point_B.x}_{self.point_B.y}"
    
    def get_diff(self):
        return Coordinates(self.point_B.x - self.point_A.x, self.point_B.y - self.point_A.y)

def get_dict_map_by_char(map):
    dict_by_char = {}
    for x in range(len(map)):
        for y in range(len(map[0])):
            map_char = map[x][y]
            if map_char not in dict_by_char.keys():
                dict_by_char[map_char] = np.array([Coordinates(x, y)])
            else :
                dict_by_char[map_char] = np.append(dict_by_char[map_char], [Coordinates(x, y)])
    return dict_by_char

def get_proximity_zones(coordinate, dict_zones):
    proximity_zones = np.array([])
    for zone_key in dict_zones.keys():
            for zone_coord in dict_zones[zone_key]:
                if coordinate.near(zone_coord, 1, False):
                    proximity_zones = np.append(proximity_zones, [zone_key])
    return np.unique(proximity_zones)

def get_zones(key, coordinates):
    dict_zones = {}
    cpt = 0
    for coordinate in coordinates:
        proximity_zones = get_proximity_zones(coordinate, dict_zones)
        if len(proximity_zones) == 0:
            dict_zones[f"{key}{cpt}"] = np.array([coordinate])
            cpt += 1
        elif len(proximity_zones) == 1:
            dict_zones[proximity_zones[0]] = np.append(dict_zones[proximity_zones[0]], [coordinate])
        else:
            dict_zones[proximity_zones[0]] = np.append(dict_zones[proximity_zones[0]], [coordinate])
            for i in range(1, len(proximity_zones)):
                dict_zones[proximity_zones[0]] = np.append(dict_zones[proximity_zones[0]], dict_zones[proximity_zones[i]])
                del dict_zones[proximity_zones[i]]
    return dict_zones

def get_dict_map_by_zone(dict_map):
    dict_by_zone = {}
    for key in dict_map.keys():
        key_zones = get_zones(key, dict_map[key])
        for zone_key in key_zones.keys():
            dict_by_zone[zone_key] = key_zones[zone_key]
    return dict_by_zone

def get_zone_area(zone):
    return len(zone)

def get_perimeter_segments(zone):
    perimeter_segments = np.array([])
    cleaned_perimeter_segments = np.array([])
    for coordinate in zone:
        perimeter_segments = np.append(perimeter_segments, [Segment(Coordinates(coordinate.x,coordinate.y), Coordinates(coordinate.x,coordinate.y + 1))])
        perimeter_segments = np.append(perimeter_segments, [Segment(Coordinates(coordinate.x,coordinate.y), Coordinates(coordinate.x + 1,coordinate.y))])
        perimeter_segments = np.append(perimeter_segments, [Segment(Coordinates(coordinate.x + 1,coordinate.y), Coordinates(coordinate.x + 1,coordinate.y + 1))])
        perimeter_segments = np.append(perimeter_segments, [Segment(Coordinates(coordinate.x,coordinate.y + 1), Coordinates(coordinate.x + 1,coordinate.y + 1))])
    segment_counter = collections.Counter(perimeter_segments)
    for segment in segment_counter.keys():
        if segment_counter[segment] == 1:
            cleaned_perimeter_segments = np.append(cleaned_perimeter_segments, [segment])
    return cleaned_perimeter_segments

def get_zone_perimeter(zone):
    return len(get_perimeter_segments(zone))

def get_zone_value(zone):
    return get_zone_area(zone) * get_zone_perimeter(zone)

def get_total_value(zones, DEBUG = False):
    value = 0
    for zone_key in zones:
        zone_value = get_zone_value(zones[zone_key])
        value += zone_value
        if DEBUG:
            print(f"Zone {zone_key} of value : {zone_value}")
    return value

def find_corner(segment1: Segment, segment2: Segment) -> Coordinates:
    # Check if segments share a point
    if segment1.point_A == segment2.point_A:
        corner = segment1.point_A
        vec1 = segment1.get_diff()
        vec2 = segment2.get_diff()
    elif segment1.point_A == segment2.point_B:
        corner = segment1.point_A
        vec1 = segment1.get_diff()
        vec2 = Coordinates(-segment2.get_diff().x, -segment2.get_diff().y)
    elif segment1.point_B == segment2.point_A:
        corner = segment1.point_B
        vec1 = Coordinates(-segment1.get_diff().x, -segment1.get_diff().y)
        vec2 = segment2.get_diff()
    elif segment1.point_B == segment2.point_B:
        corner = segment1.point_B
        vec1 = Coordinates(-segment1.get_diff().x, -segment1.get_diff().y)
        vec2 = Coordinates(-segment2.get_diff().x, -segment2.get_diff().y)
    else:
        return None  # Segments don't share a point

    # Calculate dot product
    dot_product = vec1.x * vec2.x + vec1.y * vec2.y
    # Calculate magnitudes
    mag1 = (vec1.x ** 2 + vec1.y ** 2) ** 0.5
    mag2 = (vec2.x ** 2 + vec2.y ** 2) ** 0.5
    
    # Check if vectors are parallel (0° or 180°)
    # Using dot product formula: cos(θ) = dot_product / (mag1 * mag2)
    if abs(abs(dot_product) - (mag1 * mag2)) < 1e-10:  # Using small epsilon for float comparison
        return None
        
    return corner

def get_corners(segments) -> set:
    corners = np.array([])
    for i, segment_1 in enumerate(segments):
        for segment_2 in segments[i + 1:]:
            corner = find_corner(segment_1, segment_2)
            if corner != None:
                corners = np.append(corners, [corner])
    return corners

def get_corners_nb(sergments):
    corners = get_corners(sergments)
    corner_count = collections.Counter(corners)
    counter = 0
    for corner_coord in corner_count:
        counter += np.clip(corner_count[corner_coord], 0, 2)
    return counter

def get_zone_sides(zone):
    perimeter_segments = get_perimeter_segments(zone)
    return get_corners_nb(perimeter_segments)

def get_bulk_zone_value(zone):
    return get_zone_area(zone) * get_zone_sides(zone)

def get_bulk_total_value(zones, DEBUG = False):
    value = 0
    for zone_key in zones:
        zone_value = get_bulk_zone_value(zones[zone_key])
        value += zone_value
        if DEBUG:
            print(f"Zone {zone_key} of value : {zone_value}")
    return value

input_file = open("D:\\AdventOfCode\\12\\input.txt", "r")
map = np.array([line.strip() for line in input_file.readlines()])

begin_time = datetime.datetime.now()

dict_by_char = get_dict_map_by_char(map)
dict_by_zone = get_dict_map_by_zone(dict_by_char)
result_part1 = get_total_value(dict_by_zone)
print(result_part1)
result_part2 = get_bulk_total_value(dict_by_zone)
print(result_part2)

end_time = datetime.datetime.now()
print(f"Total execution time : {end_time - begin_time}")
