import numpy as np
import copy
import open3d as o3d
from fileUtils import get_point_cloud_from_bin_file
from drawingUtils import demo_crop_geometry, demo_manual_registration


PATH_TO_BIN_FILE = "../../data/000.bin"


if __name__ == "__main__":
    source_cloud = get_point_cloud_from_bin_file(PATH_TO_BIN_FILE)
    demo_crop_geometry(source_cloud)
    demo_manual_registration(source_cloud)
