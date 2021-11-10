import open3d as o3d
import numpy as np


def get_plane_equation(three_points: o3d.geometry.PointCloud) -> list:
    first_point, second_point, third_point = np.asarray(three_points.points)
    vector_one = third_point - first_point
    vector_two = second_point - first_point
    cp = np.cross(vector_one, vector_two)
    a, b, c = cp
    d = np.dot(cp, third_point)

    return [a, b, c, d]


def get_distance_to_all_points(point_cloud: o3d.geometry.PointCloud, plane: list) -> np.ndarray:
    numpy_point_cloud = np.asarray(point_cloud.points)
    ones_array = np.ones((numpy_point_cloud.shape[0], 1), dtype=np.float64)
    numpy_point_cloud = np.append(numpy_point_cloud, ones_array, axis=1)
    plane = np.array(plane).T

    distance = np.abs(numpy_point_cloud @ plane) / np.linalg.norm(plane)

    return distance

