from src.open3DTool.planeUtils import (
    get_plane_equation,
    get_distance_to_all_points,
    get_indexes_of_points_on_plane,
    get_main_plane_equation,
)

import numpy as np
import open3d as o3d


def test_get_OXY_plane():
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(
        np.array([[1, 2, 0], [3, 4, 0], [5, 7, 0]])
    )

    assert [0, 0, -2, 0] == get_plane_equation(point_cloud)


def test_get_OXZ_plane():
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(
        np.array([[1, 0, 2], [3, 0, 4], [5, 0, 7]])
    )

    assert [0, 2, 0, 0] == get_plane_equation(point_cloud)


def test_get_OYZ_plane():
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(
        np.array([[0, 1, 2], [0, 3, 4], [0, 5, 7]])
    )

    assert [-2, 0, 0, 0] == get_plane_equation(point_cloud)


def test_get_simple_plane():
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(
        np.array([[3, 2, 3], [10, 5, 6], [8, 4, 9]])
    )

    assert [-12, 27, 1, -21] == get_plane_equation(point_cloud)


def test_get_distance_to_all_points():
    picked_points = o3d.geometry.PointCloud()
    picked_points.points = o3d.utility.Vector3dVector(
        np.array([[1, 2, 0], [3, 4, 0], [5, 7, 0]])
    )

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(
        np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    )
    point_cloud += picked_points

    np.testing.assert_array_equal(
        np.array([3, 6, 9, 0, 0, 0]),
        get_distance_to_all_points(point_cloud, np.array(get_plane_equation(picked_points))),
    )


def test_get_indexes_of_points_on_plane():
    picked_points = o3d.geometry.PointCloud()
    picked_points.points = o3d.utility.Vector3dVector(
        np.array([[1, 2, 0], [3, 4, 0], [5, 7, 0]])
    )

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(
        np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    )
    point_cloud += picked_points
    distance = 3.0

    np.testing.assert_array_equal(
        np.array([0, 3, 4, 5]),
        get_indexes_of_points_on_plane(np.array([3, 6, 9, 0, 0, 0]), distance),
    )


def test_get_main_plane_equation():
    planes_array = np.array(
        [[1, 2, 3, 4], [1, 2, 3, 5], [1, 2, 4, 5], [1, 3, 4, 5], [2, 3, 4, 5]]
    )

    np.testing.assert_array_equal(
        np.array([1.2, 2.4, 3.6, 4.8]), get_main_plane_equation(planes_array)
    )
