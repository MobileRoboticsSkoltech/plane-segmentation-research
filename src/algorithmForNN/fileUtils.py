import open3d as o3d
import numpy as np


def get_point_cloud_from_bin_file(path_to_bin_file: str) -> o3d.geometry.PointCloud:
    """
    Function allows you to get a point cloud from a file with lidar data
    """
    point_cloud_numpy = np.fromfile(path_to_bin_file, dtype=np.float32).reshape(-1, 4)
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(point_cloud_numpy[:, :3])
    return point_cloud


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


def get_labels_from_label_format_file(path_to_label_file: str) -> np.ndarray:
    return np.fromfile(path_to_label_file, dtype=np.uint32).reshape((-1))
