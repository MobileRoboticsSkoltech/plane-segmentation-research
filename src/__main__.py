from src.open3DTool.drawingUtils import draw_and_pick_points_function


def main():
    path_to_bin_file = "data/000.bin"
    distance = 0.06
    draw_and_pick_points_function(path_to_bin_file, distance)


if __name__ == "__main__":
    main()
