import cvzone
from cvzone.ColorModule import ColorFinder
import cv2
import time
import socket

font = cv2.FONT_HERSHEY_PLAIN
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

count = 0

path = 'images/' + 'ball'

myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 120, 'smin': 46, 'vmin': 100, 'hmax': 179, 'smax': 255, 'vmax': 255}

while True:
    startTime = time.time()
    success, img = cap.read()
    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask, minArea=1000)

    if contours:
        data = contours[0]['center'][0],\
               contours[0]['center'][1],\
               int(contours[0]['area'])
        print(data)
        count = count + 1
        name = './images/' + 'ball' + '/' + str(count) + '.jpg'
        cv2.imwrite(name, img)

    imgStack = cvzone.stackImages([img, imgColor, mask, imgContour], 2, 0.5)

    newTime = time.time()
    FPS = str(int(1 / (newTime - startTime)))
    cv2.putText(imgStack, FPS, (20, 50), font, 3, (255, 0, 0), 3)
    cv2.imshow("Image", imgStack)
    cv2.waitKey(1)