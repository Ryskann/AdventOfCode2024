import numpy as np

EMPTY_MARKER = -1

def get_file_system(input):
    result = np.array([]).astype(int)
    for file_id, file_lenght in enumerate(input):
        if file_id % 2 == 0:
            result = np.append(result, np.full(int(file_lenght), int(file_id / 2)))
        else:
            result = np.append(result, np.full(int(file_lenght), EMPTY_MARKER))
    return result

def minimise_free_space(file_system):
    result_len = np.array(np.where(file_system != EMPTY_MARKER)).size
    result = np.array(file_system[:result_len])
    over_the_capacity = np.array(file_system[result_len:])
    numbers_to_dispatch = np.array(over_the_capacity[np.where(over_the_capacity != EMPTY_MARKER)])
    nb_dispatched = len(numbers_to_dispatch) - 1
    for i, block in enumerate(result):
        if block == EMPTY_MARKER:
            result[i] = numbers_to_dispatch[nb_dispatched]
            nb_dispatched -= 1
    return result

def get_group_lenght(file_id):
    return len(np.where(file_system == file_id)[0])

def find_free_space(free_space_needed, free_space_idx):
    last_read = free_space_idx[0]
    start_of_space = 0
    for i in range(1, len(free_space_idx)):
        if free_space_needed == 1:
            return last_read
        if free_space_idx[i] == last_read + 1:
            last_read = free_space_idx[i]
            if i - start_of_space + 1 == free_space_needed:
                return free_space_idx[start_of_space]
        else:
            last_read = free_space_idx[i]
            start_of_space = i
    return EMPTY_MARKER

def remove_last_empty_space(file_system):
    if file_system[-1] == EMPTY_MARKER:
        return remove_last_empty_space(file_system[:len(file_system) - 1])
    return file_system

def remove_trailling_empty_space(file_system):
    return remove_last_empty_space(file_system)

def minimise_unfragmented_free_space(file_system):
    free_start_idx = EMPTY_MARKER
    for file_id in range(max(file_system), 0, -1):
        free_space = np.where(file_system == EMPTY_MARKER)[0]
        group_length = get_group_lenght(file_id)
        free_start_idx = find_free_space(group_length, free_space)
        if not free_start_idx == EMPTY_MARKER:
            old_idx = min(np.where(file_system == file_id)[0])
            if free_start_idx < old_idx:
                for i in np.where(file_system == file_id):
                    file_system[i] = EMPTY_MARKER
                for i in range(free_start_idx, free_start_idx + group_length):
                    file_system[i] = file_id
        file_system = remove_trailling_empty_space(file_system)
    return file_system

def get_checksum(file_system):
    checksum = 0
    for i, file_id in enumerate(file_system):
        if not file_id == EMPTY_MARKER:
            checksum += i * file_id
    return checksum


input_file = open("D:\\AdventOfCode\\9\\input.txt", "r")
input = input_file.readlines()[0]

file_system = get_file_system(input)
minimised_file_system = minimise_free_space(file_system)
result_part1 = get_checksum(minimised_file_system)
print(result_part1)
minimised_unfragmented_file_system = minimise_unfragmented_free_space(file_system)
result_part2 = get_checksum(minimised_unfragmented_file_system)
print(result_part2)
