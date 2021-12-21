from src.algorithmsForPointCloud.pointCloudUtils import (
    convert_point_cloud_to_numpy_array,
)

import open3d as o3d
import numpy as np


def pick_points_utils(point_cloud: o3d.geometry.PointCloud):
    picked_visualizer = o3d.visualization.VisualizerWithEditing()
    picked_visualizer.create_window()
    picked_visualizer.add_geometry(point_cloud)
    picked_visualizer.run()
    picked_visualizer.destroy_window()
    return picked_visualizer.get_picked_points()


def get_distance_to_all_points(
    point_cloud: o3d.geometry.PointCloud, plane: np.ndarray
) -> np.ndarray:
    numpy_point_cloud = np.asarray(point_cloud.points)
    ones_array = np.ones((numpy_point_cloud.shape[0], 1), dtype=np.float64)
    numpy_point_cloud = np.append(numpy_point_cloud, ones_array, axis=1)
    plane = plane.T

    distances = np.abs(numpy_point_cloud @ plane) / np.linalg.norm(plane[:-1])

    return distances


def get_indexes_of_points_on_plane(
    distances: np.ndarray, plane_distance: np.float64
) -> np.ndarray:
    return np.where(distances <= plane_distance)[0]


def get_plane_using_SVD(points: np.ndarray) -> np.ndarray:
    centroid = points.mean(axis=0)
    points_temp = points - centroid
    _, _, V_T = np.linalg.svd(points_temp)
    normal_vector = V_T[2]
    normal_vector = np.append(normal_vector, -np.dot(normal_vector, centroid))

    return normal_vector / np.linalg.norm(normal_vector[:-1])


def segment_points_on_plane_by_picked_points(
    point_cloud: o3d.geometry.PointCloud,
    picked_points_indexes: list,
    distance: np.float64,
) -> (o3d.geometry.PointCloud, list):
    points = point_cloud.select_by_index(picked_points_indexes)
    plane_equation = get_plane_using_SVD(convert_point_cloud_to_numpy_array(points))

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
