#!/usr/bin/env python3

"""
See the `freerun.py` for much more detail and for very helpful comments on the different options
"""

import os
from harvesters.core import Harvester

from .viz_open3d import display_pointcloud_minimal


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
                display_pointcloud_minimal(point_cloud_component, texture_component, texture_rgb_component)


if __name__ == '__main__':
    freerun_minimal()
