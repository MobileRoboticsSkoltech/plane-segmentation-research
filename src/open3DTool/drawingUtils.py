from src.open3DTool.planeUtils import add_new_points
from src.algorithmForNN.fileUtils import (
    get_point_cloud_from_bin_file,
    generate_labels_and_object_files,
)

import open3d as o3d
import numpy as np


def pick_points(main_point_cloud: o3d.geometry.PointCloud) -> list:
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(main_point_cloud)
    vis.run()
    vis.destroy_window()
    return vis.get_picked_points()


def draw_and_pick_points_function(
    path_to_bin_file: str,
    path_to_save_file_label: str,
    path_to_save_file_object: str,
    distance: np.float64,
):
    point_cloud = get_point_cloud_from_bin_file(path_to_bin_file)
    point_cloud.paint_uniform_color([0.51, 0.51, 0.51])
    indexes_array = np.array([])

    while True:
        picked_points_list = pick_points(point_cloud)
        assert len(picked_points_list) == 3

        point_cloud, temp_indexes = add_new_points(
            point_cloud, picked_points_list, distance
        )
        indexes_array = np.concatenate((indexes_array, temp_indexes))

        generate_labels_and_object_files(
            len(point_cloud.points),
            indexes_array.astype(int).tolist(),
            path_to_save_file_label,
            path_to_save_file_object,
        )
