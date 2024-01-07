import cv2
from cvzone.HandTrackingModule import  HandDetector
import math

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if  hands:
        lmList = hands[0]['lmList']
        print(lmList)

        x1, y1 = lmList[5]
        x2, y2 = lmList[17]

        print(abs(x2-x1))

    cv2.imshow('game', img)
    cv2.waitKey(1)
