import sys
from workWithPointCloud import main_function_to_make_label_files

# In my opinion - objects with these labels are planes, you can expand this
ROAD_LABEL = 40
SIDEWALK_LABEL = 48
PARKING_LABEL = 44
BUILDING_LABEL = 50
TERRAIN_LABEL = 72
FENCE_LABEL = 51

PLANE_LIST = [ROAD_LABEL, SIDEWALK_LABEL, PARKING_LABEL, BUILDING_LABEL, TERRAIN_LABEL, FENCE_LABEL]

def help_message():
    print("---------------------------------------------------")
    print("The existing arguments for using the algorithm are:")
    print("-PATH_TO_DATA_FOLDER=--PATH-- : Enter the path where the folder with .bin files is located")
    print("-PATH_TO_LABEL_FOLDER=--PATH-- : Enter the path where the folder with .label files is located")
    print("-PATH_TO_NEW_LABEL_FOLDER=--PATH-- : Enter the path to the folder where you want to save the textbooks. The folder will be created by itself!")
    print("---------------------------------------------------")

# python3 main.py -PATH_TO_DATA_FOLDER=/home/pavel/dataset/sequences/00/velodyne/ -PATH_TO_LABEL_FOLDER=/home/pavel/Downloads/dataset/sequences/00/labels/ -PATH_TO_NEW_LABEL_FOLDER=/home/pavel/Documents/datalabels

if __name__ == "__main__":
    if len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "-help"):
        help_message()
    elif len(sys.argv) == 4:
        PATH_TO_DATA_FOLDER = ""
        PATH_TO_LABEL_FOLDER = ""
        PATH_TO_NEW_LABEL_FOLDER = ""

        for idx in range(1, len(sys.argv)):
            current_command = sys.argv[idx].split("=")
            if current_command[0] == "-PATH_TO_DATA_FOLDER":
                PATH_TO_DATA_FOLDER = current_command[1]
            elif current_command[0] == "-PATH_TO_LABEL_FOLDER":
                PATH_TO_LABEL_FOLDER = current_command[1]
            elif current_command[0] == "-PATH_TO_NEW_LABEL_FOLDER":
                PATH_TO_NEW_LABEL_FOLDER = current_command[1]
            else:
                raise Exception("Unknown command")

        main_function_to_make_label_files(PATH_TO_DATA_FOLDER, PATH_TO_LABEL_FOLDER, PATH_TO_NEW_LABEL_FOLDER, PLANE_LIST)
        print("Success :)")
    else:
        raise Exception("Unknown command set")