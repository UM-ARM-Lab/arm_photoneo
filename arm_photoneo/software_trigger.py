#!/usr/bin/env python3
import os
import sys
from sys import platform
from harvesters.core import Harvester

from .viz_open3d import display_color_image_if_available, display_pointcloud_if_available, display_texture_if_available

def software_trigger():
    # PhotoneoTL_DEV_<ID>
    device_id = "PhotoneoTL_DEV_InstalledExamples-basic-example"
    if len(sys.argv) == 2:
        device_id = "PhotoneoTL_DEV_" + sys.argv[1]
    print("--> device_id: ", device_id)

    if platform == "win32":
        cti_file_path_suffix = "/API/bin/photoneo.cti"
        save_last_scan_path_prefix = "C:/Users/Public"
    else:
        cti_file_path_suffix = "/API/lib/photoneo.cti"
        save_last_scan_path_prefix = "~"
    cti_file_path = os.getenv('PHOXI_CONTROL_PATH') + cti_file_path_suffix
    print("--> cti_file_path: ", cti_file_path)

    with Harvester() as h:
        h.add_file(cti_file_path, True, True)
        h.update()

        # Print out available devices
        print()
        print("Name : ID")
        print("---------")
        for item in h.device_info_list:
            print(item.property_dict['serial_number'], ' : ', item.property_dict['id_'])
        print()

        with h.create({'id_': device_id}) as ia:
            features = ia.remote_device.node_map

            #print(dir(features))
            print("TriggerMode BEFORE: ", features.PhotoneoTriggerMode.value)
            features.PhotoneoTriggerMode.value = "Software"
            print("TriggerMode AFTER: ", features.PhotoneoTriggerMode.value)

            # Order is fixed on the selected output structure. Disabled fields are shown as empty components.
            # Individual structures can enabled/disabled by the following features:
            # SendTexture, SendPointCloud, SendNormalMap, SendDepthMap, SendConfidenceMap, SendEventMap, SendColorCameraImage
            # payload.components[#]
            # [0] Texture
            # [1] TextureRGB
            # [2] PointCloud [X,Y,Z,...]
            # [3] NormalMap [X,Y,Z,...]
            # [4] DepthMap
            # [5] ConfidenceMap
            # [6] EventMap
            # [7] ColorCameraImage

            # Send every output structure
            features.SendTexture.value = True
            features.SendPointCloud.value = True
            features.SendNormalMap.value = True
            features.SendDepthMap.value = True
            features.SendConfidenceMap.value = True
            #features.SendEventMap.value = True         # MotionCam-3D exclusive
            #features.SendColorCameraImage.value = True # MotionCam-3D Color exclusive

            ia.start()

            # Trigger frame by calling property's setter.
            # Must call TriggerFrame before every fetch.
            features.TriggerFrame.execute() # trigger first frame
            with ia.fetch(timeout=10.0) as buffer:
                # grab first frame
                # do something with first frame
                print(buffer)

                """
                # Save last scan to a specific file format.
                # Supported file formats are:
                # Text file (*.txt)
                # Stanford's PLY (*.ply)
                # Leica's PTX (*.ptx)
                # Photoneo's Raw data format (*.praw)
                # Raw images data format in tif (*.tif)

                # 'SaveLastScanFilePath' - Path where the file should be saved.
                #     Absolute path is preferred (e.g. C:/Users/Public/my.praw, /home/<user>/my.praw),
                #     relative path points to PhoXiControl's path (folder must exist).
                # 'SaveLastScanFrameId' - Save only if last scan has the same frame index.
                # 'SaveLastScanJsonOptions' - (optional) Configure save operations with options. Format:
                #     A simple list of options in json format where a key matches an option in GUI.
                #     Key uses the same type as in GUI, e.g. boolean, int, string, ..
                #     If the string key does not match the existing option, the option is ignored.

                save_last_scan_path = save_last_scan_path_prefix + "/test.praw"
                print("--> save_last_scan_path: ", save_last_scan_path)
                features.SaveLastScanFilePath.value = save_last_scan_path

                features.SaveLastScanFrameId.value= -1

                json_options = '{"UseCompression": true}'
                features.SaveLastScanJsonOptions.value = json_options

                features.SaveLastScan.execute()
                """

                # The buffer object will automatically call its dto once it goes
                # out of scope and releases internal buffer object.

            features.TriggerFrame.execute() # trigger second frame
            with ia.fetch(timeout=10.0) as buffer:
                # grab second frame
                # do something with second frame
                payload = buffer.payload

                texture_component = payload.components[0]
                display_texture_if_available(texture_component)

                texture_rgb_component = payload.components[1]
                display_color_image_if_available(texture_rgb_component, "TextureRGB")
                color_image_component = payload.components[7]
                display_color_image_if_available(color_image_component, "ColorCameraImage")

                point_cloud_component = payload.components[2]
                norm_component = payload.components[3]
                display_pointcloud_if_available(point_cloud_component, norm_component, texture_component, texture_rgb_component)

                # The buffer object will automatically call its dto once it goes
                # out of scope and releases internal buffer object.

            """
            # also possible use with error checking:
            features.TriggerFrame.execute() # trigger third frame
            buffer = ia.try_fetch(timeout=10.0) # grab newest frame
            if buffer is None:
                # check if device is still connected
                is_connected = features.IsConnected.value
                if not is_connected:
                    sys.exit('Device disconnected!')
            # ...
            # work with buffer
            # ...
            # release used buffer (only limited buffers available)
            buffer.queue()
            """

            # The ia object will automatically call its dtor
            # once it goes out of scope.

        # The h object will automatically call its dtor
        # once it goes out of scope.

# Call the main function
software_trigger()
