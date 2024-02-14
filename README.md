# arm_photoneo

This repository contains two packages:

1. `arm_photoneo` which is a Python-only package that does not depend on ROS, only the Phoxi Control API.
2. `arm_photoneo_ros2` which is ROS2 C++ package that depends on ROS2 (currently Humble) and the Phoxi Control API.

If you want to be able to use RViz and other ROS2 tools to process the images/pointclouds, then you'll need to use `arm_photonoeo_ros2`.

# Quickstart

Run PhoXiControl
```bash
PHOXI_WITHOUT_DISPLAY=ON ./bin/PhoXiControl
```

Run you application
```bash
python3 ./freerun_minimal.py
```

# Installation & Setup

## Installation

Install the Phoxi Control by filling out the request form on their website, which will send you an email with a download link.

## Setup

Setup the network configuration based on the recommendations in the Manual.

The current IP address of the camera is on a label on the back of the camera, as is the Serial Number.
