def is_sorted(line):
    return line == sorted(line) or line == list(reversed(sorted(line)))

def have_smooth_levels(line):
    for i in range(len(line) - 1):
        level_difference = abs(line[i] - line[i + 1])
        if(level_difference < 1 or level_difference > 3):
            return False
    return True

def is_safe_as_is(line):
    return is_sorted(line) and have_smooth_levels(line)

def is_safe(line):
    if is_safe_as_is(line):
        return True
    else:
        for i in range(len(line)):
            test_line = line.copy()
            del test_line[i]
            if is_safe_as_is(test_line):
                return True
        return False

input = open("D:\\AdventOfCode\\2\\input.txt", "r")
input_lines = input.readlines()
input_list = list(map(lambda line : [int(s) for s in line.split() if s.isdigit()], input_lines))

result_part1 = list(map(lambda line : is_safe_as_is(line), input_list)).count(True)
print(result_part1)

result_part2 = list(map(lambda line : is_safe(line), input_list)).count(True)
print(result_part2)