from src.algorithmsForPointCloud.pointCloudUtils import (
    get_calibration_matrix_from_calib_file,
    get_position_matrices_from_poses_file,
    convert_point_cloud_to_numpy_array,
)
from src.algorithmsForPointCloud.fileUtils import (
    get_point_cloud_from_bin_file,
)

import numpy as np
import open3d as o3d

import pytest


def test_get_calibration_matrix_from_file():
    path_to_calibration_file = "tests/data/calib_test_file.txt"
    correct_matrix = np.array(
        [
            [4.27680239e-04, -9.99967248e-01, -8.08449168e-03, -1.19845993e-02],
            [-7.21062651e-03, 8.08119847e-03, -9.99941316e-01, -5.40398473e-02],
            [9.99973865e-01, 4.85948581e-04, -7.20693369e-03, -2.92196865e-01],
            [0.00000000e00, 0.00000000e00, 0.00000000e00, 1.00000000e00],
        ]
    )

    np.testing.assert_array_almost_equal(
        correct_matrix, get_calibration_matrix_from_calib_file(path_to_calibration_file)
    )


def test_get_poses_line_from_file():
    path_to_poses_file = "tests/data/poses_test_file.txt"
    frame_number = 0
    correct_first_matrix = np.array(
        [
            [1.00000e00, 9.31323e-10, -3.27418e-11, 0.00000e00],
            [-9.31323e-10, 1.00000e00, -4.65661e-10, 7.45058e-09],
            [1.09139e-11, -9.31323e-10, 1.00000e00, 0.00000e00],
            [0.00000e00, 0.00000e00, 0.00000e00, 1.00000e00],
        ]
    )
    correct_second_matrix = np.array(
        [
            [0.999991, -0.00316351, -0.00274942, -0.00135393],
            [0.00316045, 0.999994, -0.00111659, -0.0248245],
            [0.00275294, 0.00110789, 0.999996, 0.672716],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    function_list_of_matrices = get_position_matrices_from_poses_file(
        path_to_poses_file
    )

    np.testing.assert_array_almost_equal(
        correct_first_matrix,
        function_list_of_matrices[0],
    )
    np.testing.assert_array_almost_equal(
        correct_second_matrix,
        function_list_of_matrices[1],
    )
