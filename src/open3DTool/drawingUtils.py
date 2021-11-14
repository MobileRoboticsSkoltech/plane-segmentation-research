from src.open3DTool.planeUtils import add_new_points
from src.open3DTool.Visualizer import Visualizer

import open3d as o3d
import numpy as np


def draw_and_pick_points_function(
    path_to_bin_file: str,
    path_to_save_file_label: str,
    path_to_save_file_object: str,
    distance: np.float64,
):
    vis = Visualizer(
        path_to_bin_file, path_to_save_file_label, path_to_save_file_object, distance
    )
    vis.run()
