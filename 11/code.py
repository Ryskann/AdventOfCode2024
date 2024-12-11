import numpy as np
from enum import Enum

def flatten(xss):
    return [x for xs in xss for x in xs]

def get_stones(input):
    return np.array([int(stone) for stone in input.split(' ')])

def handle_blink_on_stone(stone):
    stone_lenght = len(str(stone))
    if stone == 0:
        return [1]
    if stone_lenght % 2 == 0:
        return [int(str(stone)[:int(stone_lenght / 2)]), int(str(stone)[int(stone_lenght / 2):])]
    return [stone * 2024]

def handle_blinks_on_stones(stones, number_of_blinks = 1):
    for i in range(number_of_blinks):
        stones = flatten(list(map(handle_blink_on_stone, stones)))
    return stones

def stones_to_dict(stones):
    result_stones = {}
    for stone in stones:
        result_stones[stone] = 1
    return result_stones

def handle_blinks_on_stones_with_dict(stones, number_of_blinks = 1):
    stones = stones_to_dict(stones)
    for i in range(number_of_blinks):
        new_stones = {}
        for stone_value in stones.keys():
            values_for_stone_value = handle_blink_on_stone(stone_value)
            for new_value in values_for_stone_value:
                if new_value in new_stones.keys():
                    new_stones[new_value] = new_stones[new_value] + stones[stone_value]
                else :
                    new_stones[new_value] = stones[stone_value]
        stones = new_stones
    return stones

def count_total(dict):
    cpt = 0
    for key in dict.keys():
        cpt += dict[key]
    return cpt

input_file = open("D:\\AdventOfCode\\11\\input.txt", "r")
stones = np.array([get_stones(line) for line in input_file.readlines()][0])
result_part1 = len(handle_blinks_on_stones(stones, 25))
print(result_part1)

result_part2 = count_total(handle_blinks_on_stones_with_dict(stones, 75))
print(result_part2)
