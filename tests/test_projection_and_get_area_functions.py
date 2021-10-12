from src.algorithmForNN.pointCloudUtils import (
    project_point_from_point_cloud_to_2d_plane_point_cloud,
    convert_numpy_array_to_point_cloud,
    get_area_of_plane,
)

import numpy as np
import open3d as o3d

import pytest


def test_OXY_projection():
    default_plane = [0, 0, 1, 0]
    points_array = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]])
    correct_numpy_array = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0], [1.0, 0.0]])
    result_numpy_array = project_point_from_point_cloud_to_2d_plane_point_cloud(
        convert_numpy_array_to_point_cloud(points_array), default_plane
    )
    np.testing.assert_array_equal(correct_numpy_array, result_numpy_array)


def test_OXZ_projection():
    default_plane = [0, 1, 0, 0]
    points_array = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]])
    correct_numpy_array = np.array([[0.0, 1.0], [0.0, 1.0], [1.0, 1.0], [1.0, 1.0]])
    result_numpy_array = project_point_from_point_cloud_to_2d_plane_point_cloud(
        convert_numpy_array_to_point_cloud(points_array), default_plane
    )
    np.testing.assert_array_equal(correct_numpy_array, result_numpy_array)


def test_OYZ_projection():
    default_plane = [1, 0, 0, 0]
    points_array = np.array([[0, 0, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1]])
    correct_numpy_array = np.array([[0.0, 1.0], [1.0, 1.0], [1.0, 1.0], [0.0, 1.0]])
    result_numpy_array = project_point_from_point_cloud_to_2d_plane_point_cloud(
        convert_numpy_array_to_point_cloud(points_array), default_plane
    )
    np.testing.assert_array_equal(correct_numpy_array, result_numpy_array)


def test_get_area_of_projection_of_cube_on_OXY():
    OXY = [0, 0, 1, 0]
    cube = np.array(
        [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1],
        ]
    )
    area_of_square = get_area_of_plane(convert_numpy_array_to_point_cloud(cube), OXY)
    assert area_of_square == 1.0


def test_get_area_of_projection_of_prisma_on_OXY():
    OXY = [0, 0, 1, 0]
    cube = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1]])
    area_of_square = get_area_of_plane(convert_numpy_array_to_point_cloud(cube), OXY)
    assert area_of_square == 1.0
