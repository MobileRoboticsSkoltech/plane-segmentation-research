from src.algorithmForNN.pointCloudUtils import (
    get_calibration_matrix_from_calib_file,
    get_position_from_poses_file,
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
    correct_matrix = np.array(
        [
            [1.00000e00, 9.31323e-10, -3.27418e-11, 0.00000e00],
            [-9.31323e-10, 1.00000e00, -4.65661e-10, 7.45058e-09],
            [1.09139e-11, -9.31323e-10, 1.00000e00, 0.00000e00],
            [0.00000e00, 0.00000e00, 0.00000e00, 1.00000e00],
        ]
    )

    np.testing.assert_array_almost_equal(
        correct_matrix, get_position_from_poses_file(path_to_poses_file, frame_number)
    )
