## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##              Align Depth to Color               ##
#####################################################

# First import the library
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2
from collections import deque
import argparse

import realsense
import zoom_function
import color_HSV
import ball_detection
import image_capture

cam_setup = realsense.realsense_setup()
cam_start = realsense.realsense_start()
clipping_distance, align, pipeline = cam_setup.set_up()
ball_detect = ball_detection.ball_detect()
image_cap = image_capture.image()

# Streaming loop
try:
    while True:
        bg_removed, color_image = cam_start.realsense_start(pipeline, align, clipping_distance)

        img = image_cap.image_capture(bg_removed, color_image)
        basket_1_ball, frame = ball_detect.detect(img)

        print(basket_1_ball)

        basket_image_1 = np.vstack((frame[2], frame[1], frame[0]))
        images = np.hstack((bg_removed, color_image))

        cv2.imshow("color frame", images)
        cv2.imshow("basket1", basket_image_1)

        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()