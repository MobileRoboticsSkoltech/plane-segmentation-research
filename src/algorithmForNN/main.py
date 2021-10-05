import argparse
from pointCloudUtils import create_all_label_files_by_folder

# In my opinion - objects with these labels are planes, you can expand this
ROAD_LABEL = 40
SIDEWALK_LABEL = 48
PARKING_LABEL = 44
BUILDING_LABEL = 50
TERRAIN_LABEL = 72
FENCE_LABEL = 51

COUNT_OF_POINTS_PER_PLANE = 1000
AREA_OF_EACH_PLANE = 10

PLANE_LIST = [ROAD_LABEL, SIDEWALK_LABEL, PARKING_LABEL, BUILDING_LABEL, TERRAIN_LABEL, FENCE_LABEL]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-PATH_TO_DATA_FOLDER",
                        type=str,
                        help="Enter the path where the folder with .bin files is located",
                        dest="PATH_TO_DATA_FOLDER",
                        required=True)
    parser.add_argument("-PATH_TO_LABEL_FOLDER",
                        type=str,
                        help="Enter the path where the folder with .label files is located",
                        dest="PATH_TO_LABEL_FOLDER",
                        required=True)
    parser.add_argument("-PATH_TO_NEW_LABEL_FOLDER",
                        type=str,
                        help="Enter the path to the folder where you want to save the textbooks. The folder will be "
                             "created by itself!",
                        dest="PATH_TO_NEW_LABEL_FOLDER",
                        required=True)
    args = parser.parse_args()

    PATH_TO_DATA_FOLDER = args.PATH_TO_DATA_FOLDER
    PATH_TO_LABEL_FOLDER = args.PATH_TO_LABEL_FOLDER
    PATH_TO_NEW_LABEL_FOLDER = args.PATH_TO_NEW_LABEL_FOLDER

    create_all_label_files_by_folder(PATH_TO_DATA_FOLDER, PATH_TO_LABEL_FOLDER, PATH_TO_NEW_LABEL_FOLDER, PLANE_LIST,
                                     COUNT_OF_POINTS_PER_PLANE, AREA_OF_EACH_PLANE)
    print("Success :)")
