## **What is this?**

This module is an algorithm for generating semi-labeled clouds so that later they can be used in other tools. 

## **How do I use this?**

1. Install the required pip packages 
   ```bash
   $ python -m pip install -r requirements.txt
   ```
2. Run the algorithm with the required parameters. In order to get help or find out what parameters there are, you can call the help command:
   ```bash
   $ python main.py -h
   ```

Possible parameters: 

```bash
  -h, --help            show this help message and exit
  --path_to_data_folder PATH_TO_DATA_FOLDER
                        Enter the path where the folder with .bin files is
                        located.
  --path_to_label_folder PATH_TO_LABEL_FOLDER
                        Enter the path where the folder with label files is
                        located.
  --path_to_new_label_folder PATH_TO_NEW_LABEL_FOLDER
                        Enter the path to the folder where you want to save
                        the file with new labels.
  --minimum_count_of_points_per_plane MINIMUM_COUNT_OF_POINTS_PER_PLANE
                        The minimum number of points on the plane to segment
                        it.
  --minimum_area_of_per_plane MINIMUM_AREA_OF_PER_PLANE
                        The minimum area of a plane to segment it.
```

## **Usage example**

```bash
$ python main.py --path_to_data_folder /home/pavel/dataset/sequences/00/velodyne \ 
  --path_to_label_folder /home/pavel/dataset/sequences/00/labels \
  --path_to_new_label_folder home/pavel/result \
  --minimum_count_of_points_per_plane 1000 \
  --minimum_area_of_per_plane 0.8
```

In this example, folder `/home/pavel/dataset/sequences/00/labels` contains .label files, which were downloaded from [SemanticKITTI site](http://www.semantic-kitti.org/dataset.html#download). And folder `path_to_new_label_folder` is a new place where new files with labels obtained as a result of the algorithm's work will be.


## **What's interesting inside?**

As you can see, there is a `minimum_area_of_per_plane` parameter. It is not very easy to search for the area of a plane in a 3-dimensional space, as there are some outliers and etc. To solve this problem, two functions were made: 

* **Projection of points onto a plane along the plane normal vector and get 2d coords** - *`pointCloudUtils.project_point_from_point_cloud_to_2d_plane_point_cloud`*
  
  To demonstrate how it works, consider a simple example of the projection of a 3-dimensional cube onto the OXY plane:
  ```python
  OXY = [0, 0, 1, 0]
  points = np.array(
    [
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ]
  )
  project_point_from_point_cloud_to_2d_plane_point_cloud(
    convert_numpy_array_to_point_cloud(points), OXY
  )
  ```

  The result of the work will be: 
  ```python
  np.array([[0., 0.],
       [0., 0.],
       [0., 1.],
       [0., 1.],
       [1., 0.],
       [1., 0.],
       [1., 1.],
       [1., 1.]])
  ```

  As you can see, the algorithm dropped the z coordinate and returned the projected coordinates of the points to the OXY plane. 

* **Getting the area of the plane obtained as a result of the RANSAC algorithm** - *`pointCloudUtils.get_area_of_plane`*

  Internally, this algorithm uses the previous function and the [Convex Hull algorithm](https://en.wikipedia.org/wiki/Convex_hull_algorithms) (we approximate by rectangle).

  Let's consider a simple example of finding the approximate area of a 3-dimensional prism projected onto OXY.

  ```python
  OXY = [0, 0, 1, 0]
  prisma = np.array([[0, 0, 0], 
                   [1, 0, 0], 
                   [0, 1, 0], 
                   [0, 0, 1], 
                   [1, 0, 1], 
                   [0, 1, 1]])
  area_of_prisma_projected_on_OXY = get_area_of_plane(
    convert_numpy_array_to_point_cloud(points), OXY
  )
  ```

  As a answer, we get `1.0.` because by projecting the prism onto the OXY plane, we got an isosceles right-angled triangle. If we approximate it with a rectangle, then we get a square with side 1. 

## **How does it all work together?**

Consider a theoretical point cloud with a road that has a curb: 

<p align="center">
    <img src="https://s9.gifyu.com/images/Peek-2021-10-15-16-39.gif"/>
</p>

**Parameters used to segment planes:**
* `minimum_count_of_points_per_plane = 1000`
* `minimum_area_of_per_plane = 0.8`

Using these parameters, we will be able to extract only two planes. In the next image, those points that we managed to segment are marked in gray:

<p align="center">
    <img src="https://s9.gifyu.com/images/Peek-2021-10-15-16-49.gif"/>
</p>