# Plane segmentation research

[![Unit tests](https://github.com/MobileRoboticsSkoltech/plane-segmentation-research/actions/workflows/unitTestCI.yml/badge.svg?branch=master)](https://github.com/MobileRoboticsSkoltech/plane-segmentation-research/actions/workflows/unitTestCI.yml)

# Description

This repository contains materials for researching semantic and instance plane segmentation from point clouds collected from LiDARs.  

# Content

- src
  - algorithmsForPointCloud - this folder contains files with methods that allow you to transform point clouds, extract some information from them and label files.
  - open3DTool - this folder contains an MVP application containing: presegmentation by planar labels, segmenting planes by n points.
- notebooks
  - About_segment_plane - some information about segment_plane method from the Open3D library 
  - Some_functions - some set of functions for working with point clouds 
  - LeastSquaresFitting - implementation of linear regression and SVD-fitting methods to solve an optimization problem, as well as a few examples.

# Running unit tests 

1. Installing packages for testing
    ```shell
    python3 -m pip install -r requirements.txt
    ```
2. Running unit tests
    ```shell
    python3 ./scripts/run_tests.py
    ```
   
# Installing packages for src folders

1. Go to the required directory
  ```shell
  cd src/algorithmsForPointCloud
  or
  cd src/open3DTool
  ```
2. Install required packages
  ```shell
  python3 -m pip install -r requirements.txt
  ```
3. A detailed README can be found in each of the directories

# Example of running Open3DTool
```shell
python -m src --path_to_bin_file data/000.bin \
        --path_to_save_label_file data/labelFile.pcd.labels \
        --path_to_save_object_file data/labelFile.pcd.objects \
        --path_to_pcd_file data/000.pcd \ 
        --distance_to_plane 0.06 \
        --count_points_to_pick 5
```
