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

class Machine:
    def __init__(self, goal_coord, a_coord, a_cost, b_coord, b_cost):
        self.goal_coord = goal_coord
        self.a_coord = a_coord
        self.a_cost = a_cost
        self.b_coord = b_coord
        self.b_cost = b_cost
    
    def __str__(self):
        return f"Goal {self.goal_coord}\nA {self.a_coord} - cost {self.a_cost}\nB {self.b_coord} - cost {self.b_cost}"
    
    def get_score(self):
        """
        max_of_b = min(math.floor(self.goal_coord.x / self.b_coord.x), math.floor(self.goal_coord.y / self.b_coord.y))
        for nb_of_b in range(max_of_b, 0, -1):
            b_position = self.b_coord.multiply(nb_of_b)
            a_goal = self.goal_coord.minus(b_position)
            a_x_need = a_goal.x / self.a_coord.x
            a_y_need = a_goal.y / self.a_coord.y
            if a_x_need == a_y_need and a_x_need % 1 == 0:
                return True, int(nb_of_b * self.b_cost + a_x_need * self.a_cost)
        return False, 0
        """
        def solve_integer_equations(A, B):
            # Solve the system of equations
            solution = np.linalg.solve(A, B)
            
            # Check if all solutions are (close to) integers
            # Using np.isclose to handle floating-point precision issues
            integer_solution = np.round(solution)
            if np.allclose(solution, integer_solution):
                return integer_solution.astype(int)
            else:
                raise ValueError("No integer solution exists for this system of equations")
        
        system_input = np.array([[self.a_coord.x, self.b_coord.x], [self.a_coord.y, self.b_coord.y]])
        system_goal = np.array([self.goal_coord.x, self.goal_coord.y])
        try:
            solution = solve_integer_equations(system_input, system_goal)
            if self.a_coord.x * solution[0] + self.b_coord.x * solution[1] == self.goal_coord.x and self.a_coord.y * solution[0] + self.b_coord.y * solution[1] == self.goal_coord.y:
                return True, solution[0] * self.a_cost + solution[1 * self.b_cost]
            return False, 0
        except ValueError as e:
            return False, 0
        

def get_button_input_line_coord(input_line):
    coords = input_line.split(": ")[1].split(", ")
    x_value = int(coords[0].split("+")[1])
    y_value = int(coords[1].split("+")[1])
    return Coordinates(x_value, y_value)

def get_goal_input_line_coord(input_line, GOAL_ERROR = 0):
    coords = input_line.split(": ")[1].split(", ")
    x_value = int(coords[0].split("=")[1]) + GOAL_ERROR
    y_value = int(coords[1].split("=")[1]) + GOAL_ERROR
    return Coordinates(x_value, y_value)

def create_machine(machine_input, GOAL_ERROR = 0):
    A_COST = 3
    B_COST = 1
    a_coord = get_button_input_line_coord(machine_input[0])
    b_coord = get_button_input_line_coord(machine_input[1])
    goal_coord = get_goal_input_line_coord(machine_input[2], GOAL_ERROR)
    return Machine(goal_coord, a_coord, A_COST, b_coord, B_COST)

def get_machines(input, GOAL_ERROR = 0):
    GROUP_SIZE = 4
    machines_input_list = [input[n:n+GROUP_SIZE] for n in range(0, len(input), GROUP_SIZE)]
    machines_list = [create_machine(machine_input, GOAL_ERROR) for machine_input in machines_input_list]
    return machines_list

def get_total_score(machines, DEBUG = False):
    total_score = 0
    total_token_spent =0
    for i, machine in enumerate(machines):
        score, token_spent = machine.get_score()
        total_score += score
        total_token_spent += token_spent
        if DEBUG:
            print(f"Machine {i} out of {len(machines)} {math.floor(i / len(machines) * 100)}% - score = {score} - token_spent = {token_spent}")
    return total_score, total_token_spent
        
begin_time = datetime.datetime.now()

input_file = open("D:\\AdventOfCode\\13\\input.txt", "r")
input = np.array([line.strip() for line in input_file.readlines()])

machines = get_machines(input)
_, result_part1 = get_total_score(machines)
print(result_part1)

machines_error = get_machines(input, 10000000000000)
_, result_part2 = get_total_score(machines_error)
print(result_part2)

end_time = datetime.datetime.now()
print(f"Total execution time : {end_time - begin_time}")
