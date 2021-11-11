from src.open3DTool.planeUtils import (
    get_plane_equation,
)

import numpy as np
import open3d as o3d


def test_get_simple_plane():
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(
        np.array([[3, 2, 3], [10, 5, 6], [8, 4, 9]])
    )

    assert [-12, 27, 1, -21] == get_plane_equation(point_cloud)
