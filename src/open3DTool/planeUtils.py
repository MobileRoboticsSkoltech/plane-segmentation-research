from itertools import combinations
import open3d as o3d
import numpy as np


def pick_points_utils(point_cloud: o3d.geometry.PointCloud):
    picked_visualizer = o3d.visualization.VisualizerWithEditing()
    picked_visualizer.create_window()
    picked_visualizer.add_geometry(point_cloud)
    picked_visualizer.run()
    picked_visualizer.destroy_window()
    return picked_visualizer.get_picked_points()


def get_plane_equation(three_points: o3d.geometry.PointCloud) -> list:
    first_point, second_point, third_point = np.asarray(three_points.points)
    vector_one = third_point - first_point
    vector_two = second_point - first_point
    cp = np.cross(vector_one, vector_two)
    a, b, c = cp
    d = -np.dot(cp, third_point)

    return [a, b, c, d]


def get_main_plane_equation(planes: np.ndarray) -> np.ndarray:
    return np.average(planes, axis=0)


def get_distance_to_all_points(
    point_cloud: o3d.geometry.PointCloud, plane: np.ndarray
) -> np.ndarray:
    numpy_point_cloud = np.asarray(point_cloud.points)
    ones_array = np.ones((numpy_point_cloud.shape[0], 1), dtype=np.float64)
    numpy_point_cloud = np.append(numpy_point_cloud, ones_array, axis=1)
    plane = plane.T

    distances = np.abs(numpy_point_cloud @ plane) / np.linalg.norm(plane)

    return distances


def get_indexes_of_points_on_plane(
    distances: np.ndarray, plane_distance: np.float64
) -> np.ndarray:
    return np.where(distances <= plane_distance)[0]


def add_new_points(
    point_cloud: o3d.geometry.PointCloud,
    picked_points_indexes: list,
    distance: np.float64,
) -> (o3d.geometry.PointCloud, list):
    planes_array = np.empty((0, 4), np.float64)

    for combination in combinations(picked_points_indexes, 3):
        current_combination = list(combination)
        current_plane = get_plane_equation(
            point_cloud.select_by_index(current_combination)
        )
        planes_array = np.append(planes_array, np.array([current_plane]), axis=0)

    plane_equation = get_main_plane_equation(planes_array)

    indexes_list = get_indexes_of_points_on_plane(
        get_distance_to_all_points(point_cloud, plane_equation),
        distance,
    )

    picked_cloud = point_cloud.select_by_index(indexes_list)
    picked_cloud.paint_uniform_color([1.0, 0, 0])

    return (
        point_cloud.select_by_index(indexes_list, invert=True) + picked_cloud,
        indexes_list,
    )
