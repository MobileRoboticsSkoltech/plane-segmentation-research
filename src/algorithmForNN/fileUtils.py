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


def generate_labels_and_object_files(
    point_cloud_size: int,
    index_list: list,
    path_to_new_label_file: str,
    path_to_new_object_file: str,
):
    """
    Function changes those lines in the file, the point with the index of which belongs to any plane
    """
    labels_list = ["["] + ["0,"] * point_cloud_size + ["]"]
    objects_string = "[]"
    for index in index_list:
        if index + 1 == point_cloud_size:
            labels_list[index + 1] = "1"
        else:
            labels_list[index + 1] = "1,"
    labels_string = ""
    for item in labels_list:
        labels_string += item

    with open(path_to_new_label_file, "wb") as label_file, open(
        path_to_new_object_file, "wb"
    ) as object_file:

        compresses_labels_string = FIC.compress(LZW.compress(labels_string))
        compressed_objects_string = FIC.compress(LZW.compress(objects_string))
        for byte in compresses_labels_string:
            label_file.write(byte)
        for byte in compressed_objects_string:
            object_file.write(byte)


def get_labels_from_label_format_file(path_to_label_file: str) -> np.ndarray:
    return np.fromfile(path_to_label_file, dtype=np.uint32).reshape((-1))
