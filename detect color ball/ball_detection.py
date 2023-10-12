import cv2
import color_HSV
import numpy as np

class ball_detect:
    def __int__(self):
        pass

    def detect(self, img):

        ball_color = color_HSV.ball_color()
        GHueL, GHueH, GSatL, GSatH, GValL, GValH = ball_color.green_color()
        RHueL, RHueH, RSatL, RSatH, RValL, RValH = ball_color.red_color()

        frame1 = []
        frame2 = []
        frame3 = []
        frame = [frame1, frame2, frame3]
        basket_1_ball = ['E', 'E', 'E']

        for f in range(3):
                frame[f] = img[f]
                hsvFrame = cv2.cvtColor(frame[f], cv2.COLOR_BGR2HSV)

                green_lower = np.array([GHueL, GSatL, GValL], np.uint8)
                green_upper = np.array([GHueH, GSatH, GValH], np.uint8)
                green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

                red_lower = np.array([RHueL, RSatL, RValL], np.uint8)
                red_upper = np.array([RHueH, RSatH, RValH], np.uint8)
                red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

                kernel = np.ones((5, 5), "uint8")

                contours_green, hierarchy_green = cv2.findContours(green_mask,
                                                       cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)

                contours_red, hierarchy_red = cv2.findContours(red_mask,
                                                       cv2.RETR_TREE,
                                                       cv2.CHAIN_APPROX_SIMPLE)

                if len(contours_green) > 0:
                    areas = [cv2.contourArea(c) for c in contours_green]
                    max_index = np.argmax(areas)
                    cnt = contours_green[max_index]
                    ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                    M = cv2.moments(cnt)

                    if M["m10"] >0 and M["m00"] > 0:
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    # only proceed if the radius meets a minimum size
                    if radius > 30:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame[f], (int(x), int(y)), int(radius),
                                   (0, 255, 255), 2)
                        cv2.circle(frame[f], center, 5, (0, 0, 255), -1)

                    basket_1_ball[f] = 'G'

                if len(contours_red) > 0:
                    areas = [cv2.contourArea(c) for c in contours_red]
                    max_index = np.argmax(areas)
                    cnt = contours_red[max_index]
                    ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                    M = cv2.moments(cnt)

                    if M["m10"] >0 and M["m00"] > 0:
                        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                    # only proceed if the radius meets a minimum size
                    if radius > 30:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame[f], (int(x), int(y)), int(radius),
                                   (0, 255, 255), 2)
                        cv2.circle(frame[f], center, 5, (0, 0, 255), -1)

                    basket_1_ball[f] = 'R'

                if len(contours_red) == 0 and len(contours_green) == 0:
                    basket_1_ball[f] = 'E'

        return basket_1_ball, frame