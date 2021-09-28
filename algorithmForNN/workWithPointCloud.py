import open3d as o3d
import numpy as np
import os

from workWithFile import write_zeros_in_file, write_ones_to_file_by_index_list

def get_point_cloud_from_bin_file(path_to_bin_file : str) -> o3d.geometry.PointCloud:
    '''
    Function allows you to get a point cloud from a file with lidar data 
    '''
    point_cloud_np = np.fromfile(path_to_bin_file, dtype=np.float32).reshape(-1, 4)[:, :3]
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(point_cloud_np[:, :3])
    return point_cloud

def convert_point_cloud_to_numpy_array(point_cloud : o3d.geometry.PointCloud) -> np.ndarray:
    '''
    Function converts a point cloud to numpy array
    '''
    return np.asarray(point_cloud.points)

def convert_numpy_to_point_cloud(numpy_array : np.ndarray) -> o3d.geometry.PointCloud:
    '''
    Function converts numpy array to a point cloud 
    '''
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(numpy_array)
    return pcd

def select_points_from_point_cloud_by_label_id(point_cloud : o3d.geometry.PointCloud, path_to_label_file : str, label_id : int) -> o3d.geometry.PointCloud:
    '''
    Function allows you to leave points in the point cloud by label 
    '''
    labels = np.fromfile(path_to_label_file, dtype=np.uint32)
    labels = labels.reshape((-1))
    pcd_point_by_id = point_cloud.select_by_index(np.where(labels == label_id)[0])
    return pcd_point_by_id

def create_point_cloud_by_label_list(point_cloud : o3d.geometry.PointCloud, path_to_label_file : str, label_list : list) -> o3d.geometry.PointCloud:
    '''
    Function allows you to get points with the labels that we need 
    '''
    numpy_arr = np.empty((0,3), float)
    for label in label_list:
        current_point_cloud = select_points_from_point_cloud_by_label_id(point_cloud, path_to_label_file, label)
        converted_to_numpy_point_cloud = convert_point_cloud_to_numpy_array(current_point_cloud)
        numpy_arr = np.append(numpy_arr, converted_to_numpy_point_cloud, axis=0)
    return convert_numpy_to_point_cloud(numpy_arr)

def segment_plane_from_point_cloud(point_cloud : o3d.geometry.PointCloud, distance : float = 0.1) -> (o3d.geometry.PointCloud, o3d.geometry.PointCloud):
    '''
    Function allows you to extract the most visible plane from the point cloud 
    param: distance - Max distance a point can be from the plane model, and still be considered an inlier.
    '''
    try:
        _, inliers = point_cloud.segment_plane(distance_threshold=distance,
                                             ransac_n=3,
                                             num_iterations=8000)
    except Exception:
        return (point_cloud, point_cloud.clear())
    inlier_cloud = point_cloud.select_by_index(inliers)
    outlier_cloud = point_cloud.select_by_index(inliers, invert=True)
    return (inlier_cloud, outlier_cloud)

def segment_all_planes_from_point_cloud(point_cloud : o3d.geometry.PointCloud, distance : float = 0.1) -> list:
    '''
    Function allows you to get all planes from a given point cloud 
    param: distance - Max distance a point can be from the plane model, and still be considered an inlier.
    '''
    all_planes = []
    inlier_cloud, outlier_cloud = segment_plane_from_point_cloud(point_cloud, distance)
    while outlier_cloud.has_points():
        all_planes.append(inlier_cloud)
        inlier_cloud, outlier_cloud = segment_plane_from_point_cloud(outlier_cloud, distance)
    if (inlier_cloud.has_points()): all_planes.append(inlier_cloud)
    
    return all_planes

def create_dictionary_of_point_cloud(point_cloud : o3d.geometry.PointCloud) -> dict:
    '''
    Function returns a dictionary of points, with which you can get indices faster 
    '''
    result_dictionary = {}
    numpy_main_point_cloud = convert_point_cloud_to_numpy_array(point_cloud)
    
    for idx, point in enumerate(numpy_main_point_cloud):
        triple = (point[0], point[1], point[2])
        result_dictionary[triple] = idx
        
    return result_dictionary

def get_indexes_of_points(current_dict : dict, temp_point_cloud : np.ndarray) -> list:
    '''
    Function finds the indices of the required points 
    '''
    index_list = []
    for point in temp_point_cloud:
        triple = (point[0], point[1], point[2])
        index_list.append(current_dict[triple])
    return index_list

def write_ones_to_file_by_index(index_list : list, path_to_new_label_file : str):
    '''
    Function writes 1 with the desired index to the file 
    '''
    file = open(path_to_new_label_file, 'r')
    list_strings = file.readlines()
    file.close()
    for index in index_list:
        list_strings[index] = "1\n"
    file = open(path_to_new_label_file, 'w')
    file.writelines(list_strings)
    file.close()

def create_label_file(current_snapshot : str, path_to_label_file : str, label_list : list, path_to_new_label_file : str):
    '''
    Function creates a file with binary labels 
    '''
    main_point_cloud = get_point_cloud_from_bin_file(current_snapshot)
    numpy_main_point_cloud = convert_point_cloud_to_numpy_array(main_point_cloud)
    write_zeros_in_file(len(numpy_main_point_cloud), path_to_new_label_file)
    current_dict = create_dictionary_of_point_cloud(main_point_cloud)
    current_point_cloud = create_point_cloud_by_label_list(main_point_cloud, path_to_label_file, label_list)
    planes_list = segment_all_planes_from_point_cloud(current_point_cloud, 0.3)
    
    for plane in planes_list:
        numpy_plane = convert_point_cloud_to_numpy_array(plane)
        index_list = get_indexes_of_points(current_dict, numpy_plane)
        write_ones_to_file_by_index(index_list, path_to_new_label_file)

def main_function_to_make_label_files(path_to_data_folder : str, path_to_label_folder : str, path_to_new_label_folder : str, label_list : list):
    '''
    Function for data folder and label folder creates a new label folder 
    '''
    if not os.path.exists(path_to_data_folder):
        raise Exception(path_to_data_folder + " :the folder does not exist")
    if not os.path.exists(path_to_label_folder):
        raise Exception(path_to_label_folder + " :the folder does not exist")
    try:
        os.mkdir(path_to_new_label_folder)
    except FileExistsError:
        print("Directory " , path_to_new_label_folder ,  " already exists")

    for entry in os.scandir(path_to_data_folder):
        if entry.is_file():
            file_index = entry.name[:-4]

            current_bin_file = path_to_data_folder + file_index + ".bin"
            current_label_file = path_to_label_folder + file_index + ".label"
            current_new_label_file = path_to_new_label_folder + "/" + file_index + ".txt"

            create_label_file(current_bin_file, current_label_file, label_list, current_new_label_file)