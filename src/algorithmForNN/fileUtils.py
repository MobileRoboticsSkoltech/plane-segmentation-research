def write_zeros_in_file(count_of_points: int, path_to_new_label_file: str):
    """
    Function creates the initial file
    """
    with open(path_to_new_label_file, 'w') as file:
        file.write('0\n' * count_of_points)


def write_ones_to_file_by_index_list(index_list: list, path_to_new_label_file: str):
    """
    Function changes those lines in the file, the point with the index of which belongs to any plane
    """
    with open(path_to_new_label_file, 'r') as file:
        list_strings = file.readlines()
    for index in index_list:
        list_strings[index] = "1\n"
    with open(path_to_new_label_file, 'w') as file:
        file.writelines(list_strings)
