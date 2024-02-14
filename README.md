# arm_photoneo

This repository contains two packages:

1. `arm_photoneo` which is a Python-only package that does not depend on ROS, only the Phoxi Control API.
2. `arm_photoneo_ros2` which is ROS2 C++ package that depends on ROS2 (currently Humble) and the Phoxi Control API.

If you want to be able to use RViz and other ROS2 tools to process the images/pointclouds, then you'll need to use `arm_photonoeo_ros2`.

