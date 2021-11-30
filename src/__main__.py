import argparse
import numpy as np
from src.open3DTool.visualizer import Visualizer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_to_bin_file",
        type=str,
        help="Enter the path where the .bin file is located.",
        dest="path_to_bin_file",
        required=True,
    )
    parser.add_argument(
        "--path_to_save_label_file",
        type=str,
        help="Enter the path to save segmented point cloud labels",
        dest="path_to_save_label_file",
        required=True,
    )
    parser.add_argument(
        "--path_to_save_object_file",
        type=str,
        help="Enter the path to save segmented point cloud objects",
        dest="path_to_save_object_file",
        required=True,
    )
    parser.add_argument(
        "--path_to_pcd_file",
        type=str,
        help="Enter the path to save new pcd format point cloud",
        dest="path_to_pcd_file",
        required=True,
    )
    parser.add_argument(
        "--distance_to_plane",
        type=np.float64,
        help="Enter the distance from the point to the plane when it still belongs to it",
        dest="distance_to_plane",
        required=True,
    )
    parser.add_argument(
        "--count_points_to_pick",
        type=np.intc,
        help="Enter the number of points you will select each time you segment the plane",
        dest="count_points_to_pick",
        required=True,
    )
    args = parser.parse_args()

    visualizer = Visualizer(
        args.path_to_bin_file,
        args.path_to_save_label_file,
        args.path_to_save_object_file,
        args.path_to_pcd_file,
        args.distance_to_plane,
        args.count_points_to_pick,
    )
    visualizer.run()


if __name__ == "__main__":
    main()
