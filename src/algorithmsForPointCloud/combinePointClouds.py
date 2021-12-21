from src.algorithmsForPointCloud.pointCloudUtils import (
    get_calibration_matrix_from_calib_file,
    get_position_matrices_from_poses_file,
    transform_positions_in_point_cloud,
)


def create_point_cloud_by_first_N_snapshots(
    path_to_dataset: str,
    first_number_of_point_cloud: int,
    last_number_of_point_cloud: int,
) -> o3d.geometry.PointCloud:
    path_to_bin_dir = os.path.join(path_to_dataset, "velodyne")
    path_to_poses_file = os.path.join(path_to_dataset, "poses.txt")
    path_to_calib_file = os.path.join(path_to_dataset, "calib.txt")

    point_cloud = o3d.geometry.PointCloud()
    calib_matrix = get_calibration_matrix_from_calib_file(path_to_calib_file)
    poses_matrices = get_position_matrices_from_poses_file(path_to_poses_file)

    for index in range(first_number_of_point_cloud, last_number_of_point_cloud + 1):
        path_to_current_point_cloud = os.path.join(
            path_to_bin_dir, str(index).zfill(6) + ".bin"
        )
        temp_point_cloud = get_point_cloud_from_bin_file(path_to_current_point_cloud)
        temp_point_cloud = transform_positions_in_point_cloud(
            calib_matrix, poses_matrices[index], temp_point_cloud
        )

        point_cloud = point_cloud + temp_point_cloud

    return point_cloud
