import open3d as o3d
import numpy as np


def get_plane_equation(three_points: o3d.geometry.PointCloud) -> list:
    first_point, second_point, third_point = np.asarray(three_points.points)
    vector_one = third_point - first_point
    vector_two = second_point - first_point
    cp = np.cross(vector_one, vector_two)
    a, b, c = cp
    d = -np.dot(cp, third_point)

    return [a, b, c, d]


def get_distance_to_all_points(
    point_cloud: o3d.geometry.PointCloud, plane: list
) -> np.ndarray:
    numpy_point_cloud = np.asarray(point_cloud.points)
    ones_array = np.ones((numpy_point_cloud.shape[0], 1), dtype=np.float64)
    numpy_point_cloud = np.append(numpy_point_cloud, ones_array, axis=1)
    plane = np.array(plane).T

    distances = np.abs(numpy_point_cloud @ plane) / np.linalg.norm(plane)

    return distances


def get_indexes_of_points_on_plane(
    distances: np.ndarray, plane_distance: np.float64
) -> list:
    return np.where(distances <= plane_distance)[0].tolist()


def add_new_points(
    point_cloud: o3d.geometry.PointCloud,
    picked_points_indexes: list,
    distance: np.float64,
) -> o3d.geometry.PointCloud:
    three_picked_points = point_cloud.select_by_index(picked_points_indexes)
    indexes_list = get_indexes_of_points_on_plane(
        get_distance_to_all_points(
            point_cloud, get_plane_equation(three_picked_points)
        ),
        distance,
    )

    picked_cloud = point_cloud.select_by_index(indexes_list)
    picked_cloud.paint_uniform_color([1.0, 0, 0])

    return point_cloud.select_by_index(indexes_list, invert=True) + picked_cloud
