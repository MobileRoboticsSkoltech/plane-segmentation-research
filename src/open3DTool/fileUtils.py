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
