from src.open3DTool.planeUtils import (
    get_distance_to_all_points,
    get_indexes_of_points_on_plane,
    get_plane_using_SVD,
)
from src.algorithmsForPointCloud.pointCloudUtils import (
    convert_point_cloud_to_numpy_array,
    convert_numpy_array_to_point_cloud,
)

import numpy as np
import open3d as o3d


def test_get_OXY_plane():
    point_cloud = np.array([[1, 2, 0], [3, 4, 0], [5, 7, 0]])

    np.testing.assert_array_equal(
        np.array([0, 0, 1, 0]), get_plane_using_SVD(point_cloud)
    )


def test_get_OXZ_plane():
    point_cloud = np.array([[1, 0, 2], [3, 0, 4], [5, 0, 7]])

    np.testing.assert_array_equal(
        np.array([0, -1, 0, 0]), get_plane_using_SVD(point_cloud)
    )


def test_get_OYZ_plane():
    point_cloud = np.array([[0, 1, 2], [0, 3, 4], [0, 5, 7]])

    np.testing.assert_array_equal(
        np.array([1, 0, 0, 0]), get_plane_using_SVD(point_cloud)
    )


def test_get_plane_with_one_noise_point():
    point_cloud = np.array([[1, 2, 0], [3, 4, 0], [5, 7, 0], [100, 100, 1]])

    np.testing.assert_array_almost_equal(
        np.array([-0.039933, 0.030053, 0.99875, -0.010493]),
        get_plane_using_SVD(point_cloud),
        6,
    )


def test_get_simple_plane():
    point_cloud = np.array([[3, 2, 3], [10, 5, 6], [8, 4, 9]])

    np.testing.assert_array_almost_equal(
        np.array([-0.405906, 0.913289, 0.033826, -0.710336]),
        get_plane_using_SVD(point_cloud),
        6,
    )


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
        get_distance_to_all_points(
            point_cloud,
            get_plane_using_SVD(convert_point_cloud_to_numpy_array(picked_points)),
        ),
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


def test_get_plane_using_SVD():
    planes_array = np.array(
        [
            [1, 2, 3],
            [3, 2, 1],
            [4, 5, 6],
        ]
    )

    np.testing.assert_array_almost_equal(
        np.array([0.40824829, -0.81649658, 0.40824829, 0.0]),
        get_plane_using_SVD(planes_array),
        6,
    )


def test_get_plane_by_5_points():
    point_cloud = np.array(
        [
            [1, 2, 0],
            [3, 4, 6],
            [5, 7, 0],
            [2, 4, 5],
            [9, 4, 2],
        ]
    )

    np.testing.assert_array_almost_equal(
        np.array([-0.280639, 0.959049, 0.038306, -3.005047]),
        get_plane_using_SVD(point_cloud),
        6,
    )


def test_get_indexes_of_segmented_points():
    plane_point_cloud = np.array(
        [
            [1, 2, 0],
            [3, 4, 6],
            [5, 7, 0],
            [2, 4, 5],
            [9, 4, 2],
        ]
    )

    other_point_cloud = np.array(
        [
            [1, 1, 3],
            [100, 100, 100],
        ]
    )

    first_point_cloud_o3d = convert_numpy_array_to_point_cloud(plane_point_cloud)
    second_point_cloud_o3d = convert_numpy_array_to_point_cloud(other_point_cloud)
    main_point_cloud = first_point_cloud_o3d + second_point_cloud_o3d
    np.testing.assert_array_equal(
        np.array([1, 3]),
        get_indexes_of_points_on_plane(
            get_distance_to_all_points(
                main_point_cloud, get_plane_using_SVD(plane_point_cloud)
            ),
            1,
        ),
    )
