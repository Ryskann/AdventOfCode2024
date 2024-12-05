import re

input = open("D:\\AdventOfCode\\3\\input.txt", "r")
input_string = str(''.join(input.readlines()))

result = 0

while(True):
    a = len(input_string)
    start_cut = input_string.find('don\'t()')
    end_cut = input_string.find('do()')
    if not end_cut == -1:
        if start_cut > end_cut :
            input_string = input_string[:end_cut] + input_string[end_cut + 4:]
        else :
            input_string = input_string[:start_cut] + input_string[end_cut + 4:]
    else:
        input_string = input_string.replace(input_string[start_cut:len(input_string)], '')
        break

digit_pattern = re.compile(r'\d{1,3}')
operation_pattern = re.compile(r'mul\(\d{1,3},\d{1,3}\)')

for operation in re.findall(operation_pattern, input_string):
    values = re.findall(digit_pattern, operation)
    result += int(values[0]) * int(values[1])

print(result)