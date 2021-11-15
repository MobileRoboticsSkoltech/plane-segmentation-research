from src.open3DTool.planeUtils import add_new_points
from src.algorithmForNN.fileUtils import (
    get_point_cloud_from_bin_file,
    generate_labels_and_object_files,
)
import numpy as np
import open3d as o3d


class Visualizer:
    point_cloud = o3d.geometry.PointCloud()
    path_to_label_file = ""
    path_to_object_file = ""
    main_visualizer = o3d.visualization.VisualizerWithKeyCallback()
    picked_visualizer = o3d.visualization.VisualizerWithEditing()
    picked_indexes = []
    distance = 0

    def __init__(
        self,
        path_to_bin_file: str,
        path_to_save_file_label: str,
        path_to_save_file_object: str,
        distance: int,
    ):
        self.point_cloud = get_point_cloud_from_bin_file(path_to_bin_file)
        self.point_cloud.paint_uniform_color([0.51, 0.51, 0.51])
        self.path_to_label_file = path_to_save_file_label
        self.path_to_object_file = path_to_save_file_object
        self.distance = distance
        self.update_label_files([])

    def update_label_files(self, indexes: list):
        generate_labels_and_object_files(
            len(self.point_cloud.points),
            indexes,
            self.path_to_label_file,
            self.path_to_object_file,
        )

    def run(self):
        self.main_visualizer = o3d.visualization.VisualizerWithKeyCallback()
        self.main_visualizer.create_window()
        self.main_visualizer.add_geometry(self.point_cloud)
        self.set_hotkeys()
        self.main_visualizer.run()
        self.main_visualizer.destroy_window()

    def get_picked_points(self):
        return self.picked_index

    def set_hotkeys(self):
        self.main_visualizer.register_key_callback(32, self.pick_points)  # Space
        self.main_visualizer.register_key_callback(
            259, self.get_previous_snapshot
        )  # Tab

    def pick_points_utils(self):
        self.picked_visualizer = o3d.visualization.VisualizerWithEditing()
        self.picked_visualizer.create_window()
        self.picked_visualizer.add_geometry(self.point_cloud)
        self.picked_visualizer.run()
        self.picked_visualizer.destroy_window()
        return self.picked_visualizer.get_picked_points()

    def pick_points(self, visualizer):
        self.main_visualizer.close()
        self.main_visualizer.destroy_window()
        indexes_of_three_points = self.pick_points_utils()
        assert len(indexes_of_three_points) == 3
        self.update_main_window_by_three_points(indexes_of_three_points)

    def get_previous_snapshot(self, visualizer):
        if len(self.picked_indexes) == 0:
            return
        self.main_visualizer.close()
        self.main_visualizer.destroy_window()

        number_of_last_indexes = self.picked_indexes[-1]
        self.picked_indexes = self.picked_indexes[:-1]
        point_cloud_len = len(self.point_cloud.points)
        last_indexes = [
            i for i in range(point_cloud_len - number_of_last_indexes, point_cloud_len)
        ]
        picked_cloud = self.point_cloud.select_by_index(last_indexes)
        picked_cloud.paint_uniform_color([0.51, 0.51, 0.51])

        self.point_cloud = picked_cloud + self.point_cloud.select_by_index(
            last_indexes, invert=True
        )
        self.run()

    def update_main_window_by_three_points(self, picked_points: list):
        self.point_cloud, temp_indexes = add_new_points(
            self.point_cloud, picked_points, self.distance
        )
        self.picked_indexes.append(len(temp_indexes))
        self.run()
