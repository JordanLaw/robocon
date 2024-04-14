from pathlib import Path
import sys
import cv2
import depthai as dai
import numpy as np
import time
import argparse
import json
import blobconverter


class setup:
    def __init__(self):
        pass

    def function_setup(self):

        # parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--model", help="Provide model name or model path for inference",
                            default='20240413/20240413_openvino_2022.1_6shave.blob', type=str)
        parser.add_argument("-c", "--config", help="Provide config path for inference",
                            default='20240413/20240413.json', type=str)
        args = parser.parse_args()

        # parse config
        configPath = Path(args.config)
        if not configPath.exists():
            raise ValueError("Path {} does not exist!".format(configPath))

        with configPath.open() as f:
            config = json.load(f)
        nnConfig = config.get("nn_config", {})

        # parse input shape
        if "input_size" in nnConfig:
            W, H = tuple(map(int, nnConfig.get("input_size").split('x')))

        # extract metadata
        metadata = nnConfig.get("NN_specific_metadata", {})
        classes = metadata.get("classes", {})
        coordinates = metadata.get("coordinates", {})
        anchors = metadata.get("anchors", {})
        anchorMasks = metadata.get("anchor_masks", {})
        iouThreshold = metadata.get("iou_threshold", {})
        confidenceThreshold = metadata.get("confidence_threshold", {})

        print(metadata)

        # parse labels
        nnMappings = config.get("mappings", {})
        labels = nnMappings.get("labels", {})

        # get model path
        nnPath = args.model
        if not Path(nnPath).exists():
            print("No blob found at {}. Looking into DepthAI model zoo.".format(nnPath))
            nnPath = str(blobconverter.from_zoo(args.model, shaves = 6, zoo_type = "depthai", use_cache=True))
        # sync outputs
        syncNN = True

        # Create pipeline
        pipeline = dai.Pipeline()

        # Define sources and outputs
        camRgb = pipeline.create(dai.node.ColorCamera)
        detectionNetwork = pipeline.create(dai.node.YoloDetectionNetwork)
        xoutRgb = pipeline.create(dai.node.XLinkOut)
        nnOut = pipeline.create(dai.node.XLinkOut)

        xoutRgb.setStreamName("rgb")
        nnOut.setStreamName("nn")

        # Properties
        camRgb.setPreviewSize(W, H)

        camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)
        # camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        camRgb.setInterleaved(False)
        camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)
        camRgb.setFps(30)

        # Network specific settings
        detectionNetwork.setConfidenceThreshold(confidenceThreshold)
        detectionNetwork.setNumClasses(classes)
        detectionNetwork.setCoordinateSize(coordinates)
        detectionNetwork.setAnchors(anchors)
        detectionNetwork.setAnchorMasks(anchorMasks)
        detectionNetwork.setIouThreshold(iouThreshold)
        detectionNetwork.setBlobPath(nnPath)
        detectionNetwork.setNumInferenceThreads(2)
        detectionNetwork.input.setBlocking(False)

        # Linking
        camRgb.preview.link(detectionNetwork.input)
        detectionNetwork.passthrough.link(xoutRgb.input)
        detectionNetwork.out.link(nnOut.input)

        # imu setting
        # Define sources and outputs
        # imu = pipeline.create(dai.node.IMU)
        # xlinkOut = pipeline.create(dai.node.XLinkOut)
        #
        # xlinkOut.setStreamName("imu")
        #
        # # enable ACCELEROMETER_RAW at 500 hz rate
        # imu.enableIMUSensor(dai.IMUSensor.ACCELEROMETER_RAW, 500)
        # # enable GYROSCOPE_RAW at 400 hz rate
        # # imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_RAW, 400)
        #
        # imu.enableIMUSensor(dai.IMUSensor.GYROSCOPE_CALIBRATED, 400)
        #
        # # it's recommended to set both setBatchReportThreshold and setMaxBatchReports to 20 when integrating in a pipeline with a lot of input/output connections
        # # above this threshold packets will be sent in batch of X, if the host is not blocked and USB bandwidth is available
        # imu.setBatchReportThreshold(1)
        # # maximum number of IMU packets in a batch, if it's reached device will block sending until host can receive it
        # # if lower or equal to batchReportThreshold then the sending is always blocking on device
        # # useful to reduce device's CPU load  and number of lost packets, if CPU load is high on device side due to multiple nodes
        # imu.setMaxBatchReports(10)
        #
        # # Link plugins IMU -> XLINK
        # imu.out.link(xlinkOut.input)

        self.device = dai.Device(pipeline)

        # Output queue for imu bulk packets
        # self.imuQueue = self.device.getOutputQueue(name="imu", maxSize=50, blocking=False)
        # self.baseTs = None

        self.qRgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
        self.qDet = self.device.getOutputQueue(name="nn", maxSize=4, blocking=False)
