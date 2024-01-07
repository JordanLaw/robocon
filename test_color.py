import cv2
import numpy as np


def nil(self):
    pass


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cv2.namedWindow('TrackBar')
cv2.createTrackbar('HueLow', 'TrackBar', 0, 255, nil)
cv2.createTrackbar('HueHigh', 'TrackBar', 0, 255, nil)
cv2.createTrackbar('SatLow', 'TrackBar', 0, 255, nil)
cv2.createTrackbar('SatHigh', 'TrackBar', 0, 255, nil)
cv2.createTrackbar('ValLow', 'TrackBar', 0, 255, nil)
cv2.createTrackbar('ValHigh', 'TrackBar', 0, 255, nil)

while True:
    success, inputImage = cap.read()
    # inputImage = cv2.cvtColor(inputImage, cv2.COLOR_RGB2HSV)

    YHueL = cv2.getTrackbarPos('HueLow', 'TrackBar')
    YHueH = cv2.getTrackbarPos('HueHigh', 'TrackBar')
    YSatL = cv2.getTrackbarPos('SatLow', 'TrackBar')
    YSatH = cv2.getTrackbarPos('SatHigh', 'TrackBar')
    YValL = cv2.getTrackbarPos('ValLow', 'TrackBar')
    YValH = cv2.getTrackbarPos('ValHigh', 'TrackBar')

    Ylow_b = np.uint8([YHueL, YSatL, YValL])
    Yhigh_b = np.uint8([YHueH, YSatH, YValH])

    Ymask = cv2.inRange(inputImage, Yhigh_b, Ylow_b)

    Ycontours, Yhierarchy = cv2.findContours(Ymask, 1, cv2.CHAIN_APPROX_NONE)

    if len(Ycontours) > 0:
        c = max(Ycontours, key=cv2.contourArea)
        M = cv2.moments(c)

        Area = cv2.contourArea(c)

        print(Area)

    cv2.drawContours(inputImage, Ycontours, -1, (0, 255, 0), 1)
    cv2.imshow('image', inputImage)
    cv2.imshow('Mask', Ymask)

    if cv2.waitKey(1) & 0xff == 27:
        break