import open3d as o3d
import numpy as np


def demo_crop_geometry(point_cloud: o3d.geometry.PointCloud):
    print("Demo for manual geometry cropping")
    print("1) Press 'Y' twice to align geometry with negative direction of y-axis")
    print("2) Press 'K' to lock screen and to switch to selection mode")
    print("3) Drag for rectangle selection,")
    print("   or use ctrl + left click for polygon selection")
    print("4) Press 'C' to get a selected geometry and to save it")
    print("5) Press 'F' to switch to freeview mode")
    point_cloud.paint_uniform_color([0.51, 0.51, 0.51])
    o3d.visualization.draw_geometries_with_editing([point_cloud])


def pick_points(point_cloud: o3d.geometry.PointCloud):
    print("")
    print("1) Please pick at least three correspondences using [shift + left click]")
    print("   Press [shift + right click] to undo point picking")
    print("2) Afther picking points, press q for close the window")
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(point_cloud)
    vis.run()
    vis.destroy_window()
    return vis.get_picked_points()


def demo_manual_registration(point_cloud: o3d.geometry.PointCloud):
    picked_id_source = pick_points(point_cloud)
    print(picked_id_source)
    print(type(picked_id_source))
