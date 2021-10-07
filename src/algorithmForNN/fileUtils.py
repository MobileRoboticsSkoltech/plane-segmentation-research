def write_ones_to_file_by_index_list(
    point_cloud_size: int, index_list: list, path_to_new_label_file: str
):
    """
    Function changes those lines in the file, the point with the index of which belongs to any plane
    """
    list_strings = ["0\n"] * point_cloud_size
    for index in index_list:
        list_strings[index] = "1\n"
    with open(path_to_new_label_file, "w") as file:
        file.writelines(list_strings)
