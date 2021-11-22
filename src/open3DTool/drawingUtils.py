from src.open3DTool.visualizer import Visualizer

import open3d as o3d
import numpy as np


def draw_and_pick_points_function(
    path_to_bin_file: str,
    path_to_save_file_label: str,
    path_to_save_file_object: str,
    path_to_pcd_file: str,
    distance_to_plane: np.float64,
    pick_points_count: np.intc,
):
    visualizer = Visualizer(
        path_to_bin_file,
        path_to_save_file_label,
        path_to_save_file_object,
        path_to_pcd_file,
        distance_to_plane,
        pick_points_count,
    )
    visualizer.run()
