from src.open3DTool.drawingUtils import draw_and_pick_points_function


def main():
    path_to_save_file_label = "data/labelFile.pcd.labels"
    path_to_save_file_object = "data/labelFile.pcd.objects"
    path_to_bin_file = "data/000.bin"
    distance = 0.06
    draw_and_pick_points_function(
        path_to_bin_file, path_to_save_file_label, path_to_save_file_object, distance
    )


if __name__ == "__main__":
    main()
