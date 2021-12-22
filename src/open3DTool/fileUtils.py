import open3d as o3d
from src.algorithmsForPointCloud.compressUtils import FIC, LZW


def update_label_files(
    point_cloud: o3d.geometry.PointCloud,
    count_of_points: int,
    path_to_pcd_file: str,
    path_to_label_file: str,
    path_to_object_file: str,  # may be add in future
    is_append_right: bool,
):
    with open(path_to_label_file, "rb") as label_file:
        bytes_array = []
        byte = label_file.read(1)
        while byte:
            bytes_array.append(byte)
            byte = label_file.read(1)

        decompressed_array = list(
            map(int, LZW.decompress(FIC.decompress(bytes_array))[1:-1].split(","))
        )

        if is_append_right:
            decompressed_array = (
                decompressed_array[count_of_points + 1 :] + [1] * count_of_points
            )
        else:
            decompressed_array = [0] * count_of_points + decompressed_array[
                :-count_of_points
            ]

        labels_string = (
            "[" + ",".join([str(label) for label in decompressed_array]) + "]"
        )
        compressed_string = FIC.compress(LZW.compress(labels_string))

    with open(path_to_label_file, "wb") as label_file:
        label_file.write(b"".join(compressed_string))

    o3d.io.write_point_cloud(path_to_pcd_file, point_cloud)
