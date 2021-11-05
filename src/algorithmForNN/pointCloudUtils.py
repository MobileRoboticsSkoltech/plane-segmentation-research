import open3d as o3d
import numpy as np
import os
from math import sqrt, pow
from scipy.spatial import ConvexHull
from scipy.ndimage.interpolation import rotate


def convert_point_cloud_to_numpy_array(
    point_cloud: o3d.geometry.PointCloud,
) -> np.ndarray:
    """
    Function converts a point cloud to numpy array
    """
    return np.asarray(point_cloud.points)


def convert_numpy_array_to_point_cloud(
    numpy_array: np.ndarray,
) -> o3d.geometry.PointCloud:
    """
    Function converts numpy array to a point cloud
    """
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(numpy_array)
    return point_cloud


def select_points_from_point_cloud_by_label_id(
    point_cloud: o3d.geometry.PointCloud, path_to_label_file: str, label_id: int
) -> o3d.geometry.PointCloud:
    """
    Function allows you to leave points in the point cloud by label
    """
    labels = get_labels_from_label_format_file(path_to_label_file)
    point_cloud_point_by_id = point_cloud.select_by_index(
        np.where(labels == label_id)[0]
    )
    return point_cloud_point_by_id


def create_point_cloud_by_label_list(
    point_cloud: o3d.geometry.PointCloud, path_to_label_file: str, label_list: list
) -> o3d.geometry.PointCloud:
    """
    Function allows you to get points with the labels that we need
    """
    numpy_array = np.empty((0, 3), np.float32)
    for label in label_list:
        current_point_cloud = select_points_from_point_cloud_by_label_id(
            point_cloud, path_to_label_file, label
        )
        converted_to_numpy_point_cloud = convert_point_cloud_to_numpy_array(
            current_point_cloud
        )
        numpy_array = np.append(numpy_array, converted_to_numpy_point_cloud, axis=0)
    return convert_numpy_array_to_point_cloud(numpy_array)


def segment_plane_from_point_cloud(
    point_cloud: o3d.geometry.PointCloud, distance: float = 0.1
) -> (o3d.geometry.PointCloud, o3d.geometry.PointCloud, list):
    """
    Function allows you to extract the most visible plane from the point cloud
    param: distance - Max distance a point can be from the plane model, and still be considered an inlier.
    """
    try:
        plane_model, inliers = point_cloud.segment_plane(
            distance_threshold=distance, ransac_n=3, num_iterations=8000
        )
    except Exception:
        return point_cloud, point_cloud.clear(), [0, 0, 0, 0]
    inlier_cloud = point_cloud.select_by_index(inliers)
    outlier_cloud = point_cloud.select_by_index(inliers, invert=True)
    return inlier_cloud, outlier_cloud, plane_model


def project_point_from_point_cloud_to_2d_plane_point_cloud(
    point_cloud: o3d.geometry.PointCloud, plane_model: list
) -> np.ndarray:
    point_cloud_numpy = convert_point_cloud_to_numpy_array(point_cloud)
    plane = np.array(plane_model[:3])
    unit_plane = plane / np.linalg.norm(plane, ord=2)
    x = np.array([1, 0, 0])
    if unit_plane[0] == 1.0 and unit_plane[1] == 0.0 and unit_plane[2] == 0.0:
        x = np.array([0, 1, 0])
    x = x - np.dot(x, unit_plane) * unit_plane
    x /= sqrt((x ** 2).sum())
    y = abs(np.cross(unit_plane, x))
    projects_points = []

    for point in point_cloud_numpy:
        projects_points.append([np.dot(point, x), np.dot(point, y)])

    projects_points = np.array(projects_points)

    return projects_points


def get_area_of_plane(points: o3d.geometry.PointCloud, plane_model: list) -> float:
    points = project_point_from_point_cloud_to_2d_plane_point_cloud(points, plane_model)

    pi2 = np.pi / 2.0

    hull_points = points[ConvexHull(points).vertices]

    edges = np.zeros((len(hull_points) - 1, 2))
    edges = hull_points[1:] - hull_points[:-1]

    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])

    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    rotations = np.vstack(
        [np.cos(angles), np.cos(angles - pi2), np.cos(angles + pi2), np.cos(angles)]
    ).T
    rotations = rotations.reshape((-1, 2, 2))

    rot_points = np.dot(rotations, hull_points.T)

    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    areas = (max_x - min_x) * (max_y - min_y)
    best_idx = np.argmin(areas)

    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((4, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)

    current_list = []
    for i in range(4):
        current_list.append(
            sqrt(pow(rval[1][0] - rval[i][0], 2) + pow(rval[1][1] - rval[i][1], 2))
        )

    current_list.sort()

    return current_list[1] * current_list[2]


def get_calibration_matrix_from_calib_file(path_to_calibration_file: str) -> np.ndarray:
    calib_matrix = np.zeros((4, 4))
    with open(path_to_calibration_file) as file:
        (
            calib_matrix[0, 0],
            calib_matrix[0, 1],
            calib_matrix[0, 2],
            calib_matrix[0, 3],
            calib_matrix[1, 0],
            calib_matrix[1, 1],
            calib_matrix[1, 2],
            calib_matrix[1, 3],
            calib_matrix[2, 0],
            calib_matrix[2, 1],
            calib_matrix[2, 2],
            calib_matrix[2, 3],
        ) = list(map(float, file.readlines()[4][4:].rstrip().split(" ")))
        calib_matrix[3, 3] = 1

    return calib_matrix


def get_position_from_poses_file(
    path_to_poses_file: str, frame_number: int
) -> np.ndarray:
    pose_matrix = np.zeros((4, 4))
    with open(path_to_poses_file) as file:
        lines = file.readlines()
        (
            pose_matrix[0, 0],
            pose_matrix[0, 1],
            pose_matrix[0, 2],
            pose_matrix[0, 3],
            pose_matrix[1, 0],
            pose_matrix[1, 1],
            pose_matrix[1, 2],
            pose_matrix[1, 3],
            pose_matrix[2, 0],
            pose_matrix[2, 1],
            pose_matrix[2, 2],
            pose_matrix[2, 3],
        ) = list(map(np.float64, lines[frame_number].rstrip().split(" ")))
        pose_matrix[3, 3] = 1

    return pose_matrix


def transform_positions_in_point_cloud(
    calib_matrix: np.ndarray, pose_matrix: np.ndarray, point_claud: np.ndarray
) -> np.ndarray:
    left_camera_matrix = np.matmul(pose_matrix, calib_matrix)

    for index, point in enumerate(point_claud):
        temp_point = np.array([[point[0], point[1], point[2], 1]]).T
        new_point = np.matmul(left_camera_matrix, temp_point)
        point_claud[index, 0], point_claud[index, 1], point_claud[index, 2] = (
            new_point[0, 0],
            new_point[1, 0],
            new_point[2, 0],
        )

    return point_claud


def create_point_cloud_by_first_N_snapshots(
    path_to_dataset: str, count_of_point_cloud: int
) -> o3d.geometry.PointCloud:
    path_to_bin_dir = os.path.join(path_to_dataset, "velodyne")
    path_to_poses_file = os.path.join(path_to_dataset, "poses.txt")
    path_to_calib_file = os.path.join(path_to_dataset, "calib.txt")
    calib_matrix = get_calibration_matrix_from_calib_file(path_to_calib_file)
    pose_matrix = get_position_from_poses_file(path_to_poses_file, 0)

    main_point_cloud = convert_point_cloud_to_numpy_array(
        get_point_cloud_from_bin_file(os.path.join(path_to_bin_dir, "000000.bin"))
    )
    main_point_cloud = transform_positions_in_point_cloud(
        calib_matrix, pose_matrix, main_point_cloud
    )

    for index in range(1, count_of_point_cloud):
        pose_matrix = get_position_from_poses_file(path_to_poses_file, index)
        temp_point_cloud = convert_point_cloud_to_numpy_array(
            get_point_cloud_from_bin_file(
                os.path.join(
                    path_to_bin_dir, "0" * (6 - len(str(index))) + str(index) + ".bin"
                )
            )
        )
        temp_point_cloud = transform_positions_in_point_cloud(
            calib_matrix, pose_matrix, temp_point_cloud
        )

        main_point_cloud = np.concatenate((main_point_cloud, temp_point_cloud))

    return convert_numpy_array_to_point_cloud(main_point_cloud)


def segment_all_planes_from_point_cloud(
    point_cloud: o3d.geometry.PointCloud,
    min_count_of_points: int,
    min_area_of_plane: float,
    distance: float = 0.1,
) -> list:
    """
    Function allows you to get all planes from a given point cloud
    param: distance - Max distance a point can be from the plane model, and still be considered an inlier.
    """
    all_planes = []
    outlier_cloud = point_cloud
    while len(outlier_cloud.points) > min_count_of_points:
        inlier_cloud, outlier_cloud, plane_model = segment_plane_from_point_cloud(
            outlier_cloud, distance
        )
        if (
            len(inlier_cloud.points) > min_count_of_points
            and get_area_of_plane(inlier_cloud, plane_model) > min_area_of_plane
        ):
            all_planes.append(inlier_cloud)

    return all_planes


def create_dictionary_of_point_cloud(point_cloud: o3d.geometry.PointCloud) -> dict:
    """
    Function returns a dictionary of points, with which you can get indices faster
    """
    result_dictionary = {}
    numpy_main_point_cloud = convert_point_cloud_to_numpy_array(point_cloud)

    for idx, point in enumerate(numpy_main_point_cloud):
        triple = (point[0], point[1], point[2])
        result_dictionary[triple] = idx

    return result_dictionary


def append_indexes_list_of_points(
    main_index_list: list, current_dict: dict, temp_point_cloud: np.ndarray
) -> list:
    """
    Function finds the indices of the required points
    """
    for point in temp_point_cloud:
        triple = (point[0], point[1], point[2])
        main_index_list.append(current_dict[triple])
    return main_index_list


def create_label_file(
    current_snapshot: str,
    path_to_label_file: str,
    label_list: list,
    path_to_new_label_file: str,
    min_count_of_points: int,
    min_area_of_plane: float,
):
    """
    Function creates a file with binary labels
    """
    main_point_cloud = get_point_cloud_from_bin_file(current_snapshot)
    point_cloud_size = len(main_point_cloud.points)
    current_dict = create_dictionary_of_point_cloud(main_point_cloud)
    current_point_cloud = create_point_cloud_by_label_list(
        main_point_cloud, path_to_label_file, label_list
    )
    planes_list = segment_all_planes_from_point_cloud(
        current_point_cloud, min_count_of_points, min_area_of_plane, 0.06
    )
    main_index_list = []

    for plane in planes_list:
        numpy_plane = convert_point_cloud_to_numpy_array(plane)
        main_index_list = append_indexes_list_of_points(
            main_index_list, current_dict, numpy_plane
        )

    write_ones_to_file_by_index_list(
        point_cloud_size, main_index_list, path_to_new_label_file
    )


def create_all_label_files_by_folder(
    path_to_data_folder: str,
    path_to_label_folder: str,
    path_to_new_label_folder: str,
    label_list: list,
    min_count_of_points: int,
    min_area_of_plane: float,
):
    """
    Function for data folder and label folder creates a new label folder
    """
    if not os.path.exists(path_to_data_folder):
        raise Exception(path_to_data_folder + " :the folder does not exist")
    if not os.path.exists(path_to_label_folder):
        raise Exception(path_to_label_folder + " :the folder does not exist")
    try:
        os.mkdir(path_to_new_label_folder)
    except FileExistsError:
        print("Directory ", path_to_new_label_folder, " already exists")

    for entry in os.scandir(path_to_data_folder):
        if entry.is_file():
            file_index = entry.name[:-4]

            current_bin_file = path_to_data_folder + file_index + ".bin"
            current_label_file = path_to_label_folder + file_index + ".label"
            current_new_label_file = (
                path_to_new_label_folder + "/" + file_index + ".txt"
            )

            create_label_file(
                current_bin_file,
                current_label_file,
                label_list,
                current_new_label_file,
                min_count_of_points,
                min_area_of_plane,
            )
