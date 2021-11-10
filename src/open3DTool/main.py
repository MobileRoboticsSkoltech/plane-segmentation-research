import numpy as np
import copy
import open3d as o3d
from fileUtils import get_point_cloud_from_bin_file
from drawingUtils import draw_and_pick_points_function


PATH_TO_BIN_FILE = "../../data/000.bin"


if __name__ == "__main__":
    source_cloud = get_point_cloud_from_bin_file(PATH_TO_BIN_FILE)
    draw_and_pick_points_function(source_cloud)
