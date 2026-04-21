
# Lab 7: SLAM and Pure Pursuit

In this lab, you'll be implementing a Pure Pursuit implementation, which you'll use for your second race.

## Learning Goals

* Learn how to use and configure the particle filter.
* Implement the Pure Pursuit algorithm

## Lab Setup

We will build off the local file structure given in the first lab. Keep this structure in mind while you are working through the instructions!

```
${HOME}
  |
  +-- lab1_ws/              -- Lab 1 Workspace folder
  |
  +-- lab2_ws/              -- Lab 2 Workspace folder
  |
  +-- lab3_ws/              -- Lab 3 Workspace folder
  |
  +-- lab4_ws/              -- Lab 4 Workspace folder
  |
  +-- lab5_ws/              -- Lab 5 Workspace folder
  |
  +-- lab6_ws/              -- Lab 6 Workspace folder
  |
  +-- lab7_ws/              -- Lab 7 Workspace folder (NEW)
  |
  +-- sim_ws/               -- Simulator Workspace folder
```

To start with the lab, clone the repository:

```
cd ~
git clone https://github.com/unlv-f1/lab7 lab7_ws
```

Then, mount `lab7_ws` onto your Docker container, just as you've done for the previous labs. The repository contains the base code for you to get started.

## Part 1: SLAM & Particle Filter Labs

Complete the [SLAM lab](https://github.com/unlv-f1/lab-slam) and [Particle Filter lab](https://github.com/unlv-f1/lab-particle-filter).

These labs will teach you how to use SLAM to create new maps, and particle filter to localize your car on the vehicle. However, they are not strictly required to be used in the simulator.

## Part 2: Pure Pursuit

In this section, you'll implement the Pure Pursuit algorithm.

### 2-1: Specification

Develop a package named `pure_pursuit`, which implements the Pure Pursuit algorithm.

#### Running the Package

You are free to run your package by using either `ros2 launch` or `ros2 run`. You may include parameters that you think are necessary for running your node successfully.

Here is an example `ros2 run` invocation:

```
ros2 run pure_pursuit pure_pursuit_node --ros-args  \
    -p map_frame:=map  \
    -p laser_frame:=ego_racecar/laser  \
    -p base_frame:=ego_racecar/base_link  \
    -p waypoints_file_path:=waypoints/my-waypoints.csv \
    -p drive_speed_min:=1.0 \
    -p drive_speed_max:=5.0 \
    -r /odom:=/ego_racecar/odom  # remaps a topic
```

Here is an example ros2 run invocation using a parameter file. (All parameter values are stored in this file instead.)

```
ros2 run pure_pursuit pure_pursuit_node --ros-args --params-file path/to/params-file.yaml
```

#### Simulator Demonstration

Demonstrate your implementation by completing one lap around the `levine_blocked` map without collision.

#### Vehicle Demonstration

Demonstrate your implementation by completing one lap around the track without collision. The track may or may not have physical walls; if a track has virtual walls (shown with tape), you must navigate the track without touching any physical object and virtual wall.

### 2-2: Overview

Here is an overview of the workflow you'll use for running Pure Pursuit:

1. **SLAM.** Use SLAM to map the physical track.

2. **Set Waypoints**
  
     * Run `waypoints_manager` to place waypoints on the track.
     * Use `pure_pursuit` to verify if the waypoints are feasible to race with.

3. **Deploying to Vehicle Environment**
  
    * Export your waypoints file to the vehicle.
    * Launch the particle filter stack with the correct map.
    * Run `pure_pursuit` with your waypoints.

Here is an overview of the Pure Pursuit algorithm:

1. Receive odometry message

    * This represents the car's pose in the `map` frame.

2. Determine waypoint to follow

    * What if there's no waypoint that's about $L$ (lookahead) away from the car?

3. Calculate steering angle and drive speed.

4. Publish drive message.

### 2-3: Odometry Topic

Your pure pursuit algorithm's performance is based on the quality of the odometry message it receives.

In the simulator, you may use either of the following topics for your odometry topic:

* `/ego_racecar/odom`: ~100% accurate, 30 Hz
* `/pf/pose/odom`: Not 100% accurate, slower
  * Dependent on the speed of your computer

However, on the vehicle, you **must** use `/pf/pose/odom`, since it's the only topic to which odometry messages are published with respect to the map.

### 2-4: Calculating steering angle and drive speed

As shown in the lecture, the curvature of the arc to track can be calculated as:

<!-- ![](https://latex.codecogs.com/svg.latex?\gamma=\frac{2|y|}{L^2}) -->
$$\gamma=\frac{2|y|}{L^2}$$

Keep this in mind when calculating the steering angle for your car.

For drive speed, consider the following approaches:

* **Reactive**: Calculate your drive speed on the go.
* **Preset velocities**: Associate each waypoint with a speed and try to have your car match that speed.

### 2-5: Topics and Frames in Simulator vs. Vehicle Environment

Below is a table describing relevant topics and frames in the simulator environment and vehicle environment.

| .                          | Simulator Environment                  | Vehicle Environment |
| -------------------------- | -------------------------------------- | ------------------- |
| Scan topic                 | `/scan`                                | `/scan`             |
| Odometry topic (map frame) | `/ego_racecar/odom` or `/pf/pose/odom` | `/pf/pose/odom`     |
| Drive topic                | `/drive`                               | `/drive`            |
| Base frame                 | `ego_racecar/base_link`                | `base_link`         |
| Laser frame                | `ego_racecar/laser`                    | `laser`             |
| Map frame                  | `map`                                  | `map`               |

## Grading Rubric

* SLAM Lab: **30** points
* Particle Filter Lab: **30** points
* Pure Pursuit Demonstration
  * Simulator Demonstration: **20** points
  * Vehicle Demonstration: **20** points 

## Extra Resources

* A ROS 1 script for **logging waypoints** can be found [here](https://github.com/f1tenth/f1tenth_labs/blob/main/waypoint_logger/scripts/waypoint_logger.py). If you want to use it, you must adapt it to ROS 2.
* You can find some information on the markers [here](http://wiki.ros.org/rviz/DisplayTypes/Marker).
