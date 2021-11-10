import open3d as o3d
import numpy as np


def draw_point_cloud(point_cloud: o3d.geometry.PointCloud):
    point_cloud.paint_uniform_color([0.51, 0.51, 0.51])
    o3d.visualization.draw_geometries_with_editing([point_cloud])


def pick_points(point_cloud: o3d.geometry.PointCloud):
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(point_cloud)
    vis.run()
    vis.destroy_window()
    return vis.get_picked_points()


def draw_and_pick_points_function(point_cloud: o3d.geometry.PointCloud):
    point_cloud.paint_uniform_color([0.51, 0.51, 0.51])

    while True:
        picked_points_list = pick_points(point_cloud)
        assert len(picked_points_list) == 3

