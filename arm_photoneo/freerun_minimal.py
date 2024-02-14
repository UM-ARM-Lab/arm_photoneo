#!/usr/bin/env python3

"""
See the `freerun.py` for much more detail and for very helpful comments on the different options
"""

import numpy as np
import open3d as o3d
import cv2
import os
import sys
from sys import platform
from harvesters.core import Harvester

def display_pointcloud(pointcloud_comp, texture_comp, texture_rgb_comp):
    pointcloud = pointcloud_comp.data.reshape(pointcloud_comp.height * pointcloud_comp.width, 3).copy()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pointcloud)

    texture_rgb = np.zeros((pointcloud_comp.height * pointcloud_comp.width, 3))
    if texture_comp.width > 0 and texture_comp.height > 0:
        texture = texture_comp.data.reshape(texture_comp.height, texture_comp.width, 1).copy()
        texture_rgb[:, 0] = np.reshape(1/65536 * texture, -1)
        texture_rgb[:, 1] = np.reshape(1/65536 * texture, -1)
        texture_rgb[:, 2] = np.reshape(1/65536 * texture, -1)
    elif texture_rgb_comp.width > 0 and texture_rgb_comp.height > 0:
        texture = texture_rgb_comp.data.reshape(texture_rgb_comp.height, texture_rgb_comp.width, 3).copy()
        texture_rgb[:, 0] = np.reshape(1/65536 * texture[:, :, 0], -1)
        texture_rgb[:, 1] = np.reshape(1/65536 * texture[:, :, 1], -1)
        texture_rgb[:, 2] = np.reshape(1/65536 * texture[:, :, 2], -1)
    else:
        print("Texture and TextureRGB are empty!")
        return
    texture_rgb = cv2.normalize(texture_rgb, dst=None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    pcd.colors = o3d.utility.Vector3dVector(texture_rgb)
    o3d.visualization.draw_geometries([pcd], width=800,height=600)
    return


def freerun_minimal():
    device_id = "PhotoneoTL_DEV_DHV-146"

    cti_file_path_suffix = "/API/lib/photoneo.cti"
    cti_file_path = os.getenv('PHOXI_CONTROL_PATH') + cti_file_path_suffix

    with Harvester() as h:
        h.add_file(cti_file_path, True, True)
        h.update()

        with h.create({'id_': device_id}) as ia:
            features = ia.remote_device.node_map

            features.PhotoneoTriggerMode.value = "Freerun"
            features.SendTexture.value = True
            features.SendPointCloud.value = True
            features.SendNormalMap.value = False # True
            features.SendDepthMap.value = False # True
            features.SendConfidenceMap.value = False # True
            features.SendEventMap.value = False # True
            features.SendColorCameraImage.value = True

            ia.start()

            with ia.fetch(timeout=10.0) as buffer:
                payload = buffer.payload

                texture_component = payload.components[0]
                texture_rgb_component = payload.components[1]
                point_cloud_component = payload.components[2]
                display_pointcloud(point_cloud_component, texture_component, texture_rgb_component)


if __name__ == '__main__':
    freerun_minimal()
