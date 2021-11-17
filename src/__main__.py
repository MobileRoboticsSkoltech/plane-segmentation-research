import argparse
from src.open3DTool.drawingUtils import draw_and_pick_points_function


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
        dest="path_to_label_folder",
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
    args = parser.parse_args()
    distance = 0.06
    draw_and_pick_points_function(
        args.path_to_bin_file,
        args.path_to_save_label_file,
        args.path_to_save_object_file,
        args.path_to_pcd_file,
        distance,
    )


if __name__ == "__main__":
    main()
