import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics.utils import yaml_load
from ultralytics.utils.checks import check_yaml
from yolo_segmentation import YOLO_Segmentation
from yolo_segmentation import YOLO_Detection
import serial
import time

ser = serial.Serial('COM10',baudrate=115200,timeout=1)
time.sleep(0.5)
pos = 90
pos1 = 90

CLASSES = yaml_load(check_yaml('model/data_robocon_v13.yaml'))['names']
print(CLASSES)
#ys = YOLO_Segmentation("yolov8m-seg.pt")
yd = YOLO_Detection('model/best_robocon_v13.pt')
font = cv2.FONT_HERSHEY_PLAIN

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

while True:

    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    if not depth_frame or not color_frame:
        continue

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    depth_colormap_dim = depth_colormap.shape
    color_colormap_dim = color_image.shape

    # If depth and color resolutions are different, resize color image to match depth image for display
    if depth_colormap_dim != color_colormap_dim:
        resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
        images = np.hstack((resized_color_image, depth_colormap))
    else:
        images = np.hstack((color_image, depth_colormap))

    detect_image = color_image

    bboxes, class_ids, scores = yd.detect(detect_image)
    for bbox, class_id, score in zip(bboxes, class_ids, scores):
        # print("bbox:", bbox, "class id:", class_id, "score:", score)
        (x, y, x2, y2) = bbox

        if (score > 0.5 and class_id == 1):
            cv2.rectangle(detect_image, (x, y), (x2, y2), (255, 0, 0), 2)

            w = x2 - x

            errorPan = (x + w/2) - 640/2
            print('errorPan: ', errorPan)
            if abs(errorPan) > 40:
                pos = pos - errorPan / 40

            if pos > 150:
                pos = 150
                print("Out of range")

            if pos < 10:
                pos = 10
                print("Out of range")

            servoPos = 'RL' + str(pos) + '\r'
            ser.write(servoPos.encode('utf-8'))
            print('servoPos = ', servoPos)
            time.sleep(0.00001)

            h = y2 - y
            errorPan = (y + h / 2) - 480 / 2
            print('errorPan', errorPan)
            if abs(errorPan) > 40:
                pos1 = pos1 + errorPan / 40
            # print(type(pos))
            if pos1 > 170:
                pos = 170
            print("Out of range")
            if pos1 < 10:
                pos = 10
            print("out of range")
            servoPos = 'UD' + str(pos1) + '\r'
            ser.write(servoPos.encode('utf-8'))
            print('servoPos = ', servoPos)
            time.sleep(0.00001)

            point = (int((x+w/2)), int((y+h/2)))
            print(point[1])
            cv2.circle(detect_image,(point[0],point[1]),2, (0, 0, 255), -1)
            distance = int(depth_frame.get_distance(point[0], point[1]) * 1000)
            distance = (str(distance) + " mm")
            # print("distance: " + str(distance*1000))

            label = f'{CLASSES[class_id]} ({distance})'
            cv2.putText(detect_image, label, (x, y - 10), font, 2, (0, 0, 255), 2)

            time.sleep(0.00001)

    # Show images
    images = np.hstack((detect_image, depth_colormap))
    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)

    if cv2.waitKey(1) & 0xff == 27:
        break

pipeline.stop()
cv2.destoryAllWindow()
