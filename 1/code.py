input = open("D:\\AdventOfCode\\1\\input.txt", "r")
input_lines = input.readlines()
input_list = list(map(lambda line : [int(s) for s in line.split() if s.isdigit()], input_lines))

input_left = sorted(pair[0] for pair in input_list)
input_right = sorted(pair[1] for pair in input_list)

result_part1 = sum(list(map(lambda pair : abs(pair[0] - pair[1]), zip(input_left, input_right))))
print(result_part1)

result_part2 = sum(list(map(lambda left_id : left_id * input_right.count(left_id), input_left)))
print(result_part2)