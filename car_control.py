import cv2
import numpy as np
import serial
import time

ser = serial.Serial(
    port = "COM11",
    baudrate = 115200,
    timeout = 1,
    xonxoff= False,
    rtscts= False,
    dsrdtr= False)

time.sleep(0.5)

value = [0xFF, 0x00, 0x00, 0x00, 0x00, 0x00]
ser.write(serial.to_bytes(value))
print(serial.to_bytes(value))

def nil(self):
    pass


def move_command(cx):
    # move  forward
    if cx > 50 and cx < 70:
        value = [0xFF, 0x00, 0x40, 0x00, 0x00, 0x00]
        ser.write(serial.to_bytes(value))
        print("F")

    # move left
    elif cx <= 50 and cy <= 30:
        value = [0xFF, 0x40, 0x00, 0x00, 0x00, 0x00]
        ser.write(serial.to_bytes(value))
        print("L")

    # move right
    elif cx >= 70 and cy <= 30:
        value = [0xFF, 0xC9, 0x00, 0x00, 0x00, 0x00]
        ser.write(serial.to_bytes(value))
        print("R")

    # rotate left
    elif cx <= 50:
        value = [0xFF, 0x00, 0x00, 0xC0, 0x00, 0x00]
        ser.write(serial.to_bytes(value))
        print("RL")

    # rotate right
    elif cx >= 70:
        value = [0xFF, 0x00, 0x00, 0x30, 0x00, 0x00]
        ser.write(serial.to_bytes(value))
        print("RR")


def move_basket(white_area, basket,pass_numberLine, Wcontours, extTop, state, counter):
    if basket > 2:
        # move right
        if white_area >= 100:
            counter = 1

        if counter:
            counter += 1
            if counter == 3:
                pass_numberLine += 1
                counter = 0

        value = [0xFF, 0xC9, 0x00, 0x00, 0x00, 0x00]
        ser.write(serial.to_bytes(value))
        print("R1")

        if pass_numberLine == basket-2:
            if len(Wcontours) > 0 and white_area >= 1500:
                state += 1

    if basket < 2:
        # move right
        if white_area >= 100:
            counter = 1

        if counter:
            counter += 1
            if counter == 3:
                pass_numberLine += 1
                counter = 0

        value = [0xFF, 0x40, 0x00, 0x00, 0x00, 0x00]
        ser.write(serial.to_bytes(value))
        print("R1")

        if pass_numberLine == 2 - basket:
            if len(Wcontours) > 0 and white_area >= 1500:
                state += 1


    return state, pass_numberLine, counter


# Open the camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 160)
cap.set(4, 120)

# # White color
# WHueL = 255
# WHueH = 175
# WSatL = 255
# WSatH = 0
# WValL = 255
# WValH = 0

# White color
WHueL = 255
WHueH = 145
WSatL = 255
WSatH = 0
WValL = 255
WValH = 0

state = 0
basket_target = 0

pass_numberLine = 0

cx = 0
cy = 0
extLeft = []
extRight = []
extTop = []

white_area = 0
w_counter = 0

while True:
    success, frameW = cap.read()

    # crop the image restrict the view of the car (line detection needed)
    Wcrop_img = frameW[60:120, 0:130]

    # Find yellow line
    Wlow_b = np.uint8([WHueL, WSatL, WValL])
    Whigh_b = np.uint8([WHueH, WSatH, WValH])
    Wmask = cv2.inRange(Wcrop_img, Whigh_b, Wlow_b)
    Wcontours, Whierarchy = cv2.findContours(Wmask, 1, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(Wcrop_img, Wcontours, -1, (0, 255, 0), 1)

    if len(Wcontours) > 0:  # detected yellow line
        c = max(Wcontours, key=cv2.contourArea)  # find the biggest contour
        white_area = cv2.contourArea(c)
        print("area")
        print(white_area)
        M = cv2.moments(c)

        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])

        print(extLeft)
        print(extRight)
        print(extTop)

        cv2.circle(Wcrop_img, extRight, 1, (0, 255, 0), -1)
        cv2.circle(Wcrop_img, extLeft, 1, (255, 0, 0), -1)
        cv2.circle(Wcrop_img, extTop, 1, (0, 0, 255), -1)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            print("CX: " + str(cx) + " CY: " + str(cy))

            cv2.line(Wcrop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)
            cv2.line(Wcrop_img, (0, cy), (1280, cy), (255, 0, 0), 1)

    if state == 0:
        move_command(cx)

        if len(Wcontours) > 0:
            if int(extLeft[0]) <= 5 and int(extRight[0]) >= 125:
                state = 1

    if state == 1:
        move_command(cx)

        if int(extLeft[0]) <= 85 and int(extLeft[0]) > 5 and int(extRight[0]) >= 60 and int(extRight[0]) < 125:
            state = 2

    if state == 2:
        if basket_target == 2:
            state += 1
        else:
            state, pass_numberLine, w_counter = move_basket(white_area, basket_target, pass_numberLine,Wcontours, extTop, state, w_counter)


    if state == 3:
        move_command(cx)



    print(state)

    cv2.imshow('test', Wcrop_img)

    if cv2.waitKey(1) & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()