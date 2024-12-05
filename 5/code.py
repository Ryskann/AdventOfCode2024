import re
import math

input_file = open("D:\\AdventOfCode\\5\\input.txt", "r")
input = str(''.join(input_file.readlines()))

def get_rule_book(input):
    digit_pattern = re.compile(r'\d{1,2}')
    rule_pattern = re.compile(r'\d{1,2}\|\d{1,2}')
    rule_book = {}
    for rule in re.findall(rule_pattern, input):
        values = re.findall(digit_pattern, rule)
        if int(values[0]) in rule_book.keys():
            rule_book[int(values[0])] += [int(values[1])]
        else:
            rule_book.update({int(values[0]) : [int(values[1])]})
    return rule_book

def get_update_list(input):
    digit_pattern = re.compile(r'\d{1,2}')
    update_pattern = re.compile(r'([\d{2},]+\d{2})')
    update_list = []
    for update_raw in re.findall(update_pattern, input):
        update = []
        for digit in re.findall(digit_pattern, update_raw):
            update.append(int(digit))
        update_list.append(update)
    return update_list

def get_last_idx_in_list(digit, list):
    return max(idx for idx, val in enumerate(list) if val == digit)

def is_rule_correct_for_digit(list, digit_check, rule):
    lest_checked_digit_idx = get_last_idx_in_list(digit_check, list)
    for rule_digit in rule:
        if rule_digit in list:
            if lest_checked_digit_idx > list.index(rule_digit):
                return False
    return True

def is_update_correct(update, rule_book):
    for digit_check in rule_book.keys():
        if digit_check in update:
            if not is_rule_correct_for_digit(update, digit_check, rule_book[digit_check]):
                return False
    return True

def get_middle_digit(digit_list):
    return digit_list[math.floor(len(digit_list) / 2)]

def get_correct_position(put_number, start_list, rule_book):
    idx = len(start_list)
    for i, number in enumerate(start_list):
        if number in rule_book.keys():
            if put_number in rule_book[number]:
                idx = min(i, idx)
    return idx

def put_in_correct_place(put_number, start_list, rule_book):
    correct_idx = get_correct_position(put_number, start_list, rule_book)
    return start_list[:correct_idx] + [put_number] + start_list[correct_idx:]

def fix_order_by_rule_book(list, rule_book):
    ordered_list = [list[0]]
    for i in range(1, len(list)):
        ordered_list = put_in_correct_place(list[i], ordered_list, rule_book)
    return ordered_list

rule_book = get_rule_book(input)
update_list = get_update_list(input)

result_part1 = 0
result_part2 = 0
for update in update_list:
    if is_update_correct(update, rule_book):
        result_part1 += get_middle_digit(update)
    else:
        result_part2 += get_middle_digit(fix_order_by_rule_book(update, rule_book))
    
print(result_part1)
print(result_part2)
