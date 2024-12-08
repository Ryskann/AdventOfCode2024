import numpy as np
from enum import Enum

class Operators(Enum):
    def add(nb1, nb2):
        return nb1 + nb2
    
    def multiply(nb1, nb2):
        return nb1 * nb2
    
    def concat(nb1, nb2):
        return int(str(nb1) + str(nb2))

class Operation:
    def __init__(self, input_line):
        self.test_value = int(input_line.split(':')[0])
        self.numbers = np.array([int(number) for number in input_line.split(':')[1].strip().split(' ')])
    
    def __str__(self):
        return f"test value : {self.test_value}, numbers : {self.numbers}"
    
    def resolving_step(self, current_result, current_position, operators) -> bool:
        if current_position == len(self.numbers):
            return current_result == self.test_value
        for operator in operators:
            if self.resolving_step(operator(current_result, self.numbers[current_position]), current_position + 1, operators):
                return True
        return False
    
    def can_be_resolved_with_operators(self, operators) -> bool:
        return self.resolving_step(self.numbers[0], 1, operators)

def count_total_result_of_operations_that_can_be_resolved(operations, operators):
    result = 0
    for operation in operations:
        if operation.can_be_resolved_with_operators(operators):
            result += operation.test_value
    return result
        

input_file = open("D:\\AdventOfCode\\7\\input.txt", "r")
operations = np.array([Operation(line) for line in input_file.readlines()])

result_part1 = count_total_result_of_operations_that_can_be_resolved(operations, [Operators.add, Operators.multiply])
print(result_part1)

result_part2 = count_total_result_of_operations_that_can_be_resolved(operations, [Operators.add, Operators.multiply, Operators.concat])
print(result_part2)
