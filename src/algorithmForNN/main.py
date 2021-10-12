import argparse
from pointCloudUtils import create_all_label_files_by_folder

# In my opinion - objects with these labels are planes, you can expand this
ROAD_LABEL = 40
SIDEWALK_LABEL = 48
PARKING_LABEL = 44
BUILDING_LABEL = 50
TERRAIN_LABEL = 72
FENCE_LABEL = 51

PLANE_LIST = [
    ROAD_LABEL,
    SIDEWALK_LABEL,
    PARKING_LABEL,
    BUILDING_LABEL,
    TERRAIN_LABEL,
    FENCE_LABEL,
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_to_data_folder",
        type=str,
        help="Enter the path where the folder with .bin files is located.",
        dest="path_to_data_folder",
        required=True,
    )
    parser.add_argument(
        "--path_to_label_folder",
        type=str,
        help="Enter the path where the folder with label files is located.",
        dest="path_to_label_folder",
        required=True,
    )
    parser.add_argument(
        "--path_to_new_label_folder",
        type=str,
        help="Enter the path to the folder where you want to save the textbooks. The folder will be "
        "created by itself!",
        dest="path_to_new_label_folder",
        required=True,
    )
    parser.add_argument(
        "--minimum_count_of_points_per_plane",
        type=str,
        help="The minimum number of points on the plane to segment it.",
        dest="minimum_count_of_points_per_plane",
        required=True,
    )
    parser.add_argument(
        "--minimum_area_of_per_plane",
        type=str,
        help="The minimum area of a plane to segment it.",
        dest="minimum_area_of_per_plane",
        required=True,
    )
    args = parser.parse_args()

    create_all_label_files_by_folder(
        args.path_to_data_folder,
        args.path_to_label_folder,
        args.path_to_new_label_folder,
        PLANE_LIST,
        args.minimum_count_of_points_per_plane,
        args.minimum_area_of_per_plane,
    )
    print("Success :)")
