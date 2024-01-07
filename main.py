import cv2
from ultralytics.utils import yaml_load
from ultralytics.utils.checks import check_yaml
from yolo_segmentation import YOLO_Segmentation
from yolo_segmentation import YOLO_Detection
import time
import serial
import realsense
import numpy as np
from stable_baselines3 import PPO
from collections import deque

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


def var_clear():
    basket.clear()
    basket_crop.clear()
    ballstatus.clear()
    basket1ball.clear()
    basket2ball.clear()
    basket3ball.clear()
    basket4ball.clear()
    basket5ball.clear()
    basket_detail.clear()
    basket_status.clear()
    basket_full.clear()
    obs.clear()


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

    if basket == 2:
        state += 1



    return state, pass_numberLine, counter

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 160)
cap.set(4, 120)

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

def basket_check(e):
  return e['x1']

def ball_check(e):
  return e['cx']


def ball_checkloc(e):
  return e['cy']


# Set up realsense camera
cam_setup = realsense.realsense_setup()
cam_start = realsense.realsense_start()
clipping_distance, align, pipeline = cam_setup.set_up()

# ser = serial.Serial('COM7', baudrate=115200, timeout=1) # Check and change the COM port to match with your Arduino connection
time.sleep(0.5)

# Load yolo8 pre-trained model
CLASSES = yaml_load(check_yaml('model/data_robocon_v13.yaml'))['names']
yd = YOLO_Detection('model/best_robocon_v13.pt')


model = PPO.load("AI_model/20231102-ver4 (red ball first)_final.zip")

prev_actions = deque(maxlen=20)  # however long we aspire the snake to be
for i in range(20):
    prev_actions.append(-1)

font = cv2.FONT_HERSHEY_PLAIN

item = 0

ball = 0
basket = []
basket_crop = []
ballstatus = []

basket1ball = []
basket2ball = []
basket3ball = []
basket4ball = []
basket5ball = []

basket_detail = []
basket_status = []
basket_full = []

action = -1
detect_time = 0

target0 = 0
target1 = 0
target2 = 0
target3 = 0
target4 = 0

cal_target0 = 0
cal_target1 = 0
cal_target2 = 0
cal_target3 = 0
cal_target4 = 0
cal_array = 0

obs = []

while True:
    startTime = time.time()
    bg_removed, color_image = cam_start.realsense_start(pipeline, align, clipping_distance)

    while detect_time <= 25:

        # Read the image from the camera
        img = color_image

        # Get the details from the detection
        bboxes, class_ids, scores = yd.detect(img)

        for bbox, class_id, score in zip(bboxes, class_ids, scores):
            # print("bbox:", bbox, "class id:", class_id, "score:", score)

            # Get the box position of the detected object
            (x, y, x2, y2) = bbox
            numbers_box = len(bboxes)

            # Show object with specific % of con
            # Find blue ball
            if score > 0.05 and class_id == 1:
                # cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)
                item_center = [int((x + ((x2 - x) / 2))), int((y + ((y2 - y) / 2)))]
                cv2.circle(img, (item_center[0],item_center[1]), 5, (255,0,0),-1)

                # #cv2.polylines(img, [seg], True, (0, 0, 255), 4)
                # label = f'{CLASSES[class_id]} ({score:.2f})'
                # # cv2.putText(img, str(class_id), (x, y - 10), font, 2, (0, 0, 255), 2)
                # cv2.putText(img, label, (x, y - 10), font, 2, (0, 0, 255), 2)

                # Obtain the center of the object
                ball_value = {'cx': item_center[0], 'cy': item_center[1], 'color': 2}
                ballstatus.append(ball_value)

            # Find red ball
            if score > 0.01 and class_id == 3:

                # cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)
                item_center = [int((x + ((x2 - x) / 2))), int((y + ((y2 - y) / 2)))]
                cv2.circle(img, (item_center[0], item_center[1]), 5, (0, 0, 255), -1)

                # cv2.polylines(img, [seg], True, (0, 0, 255), 4)
                # label = f'{CLASSES[class_id]} ({score:.2f})'
                # cv2.putText(img, str(class_id), (x, y - 10), font, 2, (0, 0, 255), 2)
                # cv2.putText(img, label, (x, y - 10), font, 2, (0, 0, 255), 2)

                # Obtain the center of the object
                ball_value = item_center = {'cx': item_center[0], 'cy': item_center[1], 'color': 1}
                ballstatus.append(ball_value)

            # Find basket
            if score > 0.1 and class_id == 0:
                cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)
                item_center = [int((x + ((x2 - x) / 2))), int((y + ((y2 - y) / 2)))]
                cv2.circle(img, (item_center[0], item_center[1]), 5, (0, 0, 0), -1)

                # obtain the range of the basket
                basket_position = {'x1': x, 'y1': y, 'x2': x2, 'y2': y2}
                basket.append(basket_position)

        # sort the basket and the ball in the basket
        basket.sort(key=basket_check)
        ballstatus.sort(key=ball_check)

        # Put the ball value in the correct basket
        for z in range(len(ballstatus)):
            if len(basket) >= 1:
                if ballstatus[z]['cx'] >= basket[0]['x1'] and ballstatus[z]['cx'] <= basket[0]['x2']:
                    basket1ball.append(ballstatus[z])
            if len(basket) >= 2:
                if ballstatus[z]['cx'] >= basket[1]['x1'] and ballstatus[z]['cx'] <= basket[1]['x2']:
                    basket2ball.append(ballstatus[z])
            if len(basket) >= 3:
                if ballstatus[z]['cx'] >= basket[2]['x1'] and ballstatus[z]['cx'] <= basket[2]['x2']:
                    basket3ball.append(ballstatus[z])
            if len(basket) >= 4:
                if ballstatus[z]['cx'] >= basket[3]['x1'] and ballstatus[z]['cx'] <= basket[3]['x2']:
                    basket4ball.append(ballstatus[z])
            if len(basket) >= 5:
                if ballstatus[z]['cx'] >= basket[4]['x1'] and ballstatus[z]['cx'] <= basket[4]['x2']:
                    basket5ball.append(ballstatus[z])


        # sort the ball according to the y-value
        basket1ball.sort(key=ball_checkloc)
        basket2ball.sort(key=ball_checkloc)
        basket3ball.sort(key=ball_checkloc)
        basket4ball.sort(key=ball_checkloc)
        basket5ball.sort(key=ball_checkloc)

        basket_detail.append(basket1ball)
        basket_detail.append(basket2ball)
        basket_detail.append(basket3ball)
        basket_detail.append(basket4ball)
        basket_detail.append(basket5ball)

        for x in range(5):
            if len(basket_detail[x]) > 0:
                if len(basket_detail[x]) == 1:
                    basket_status.extend((basket_detail[x][0]['color'], 0, 0))
                    basket_full.append(0)
                elif len(basket_detail[x]) == 2:
                    basket_status.extend((basket_detail[x][1]['color'], basket_detail[x][0]['color'], 0))
                    basket_full.append(0)
                elif len(basket_detail[x]) == 3:
                    basket_status.extend((basket_detail[x][2]['color'], basket_detail[x][1]['color'], basket_detail[x][0]['color']))
                    basket_full.append(1)

                # else:
                #     basket_status.extend((0,0,0))
            else:
                basket_status.extend((0, 0, 0))
                basket_full.append(0)

        # Find which ball in the basket
        # if len(basket1ball) > 0:
        #     if len(basket1ball) == 1:
        #         basket1slot = [basket1ball[0]['color'], 0, 0]
        #     elif len(basket1ball) == 2:
        #         basket1slot = [basket1ball[0]['color'], basket1ball[1]['color'], 0]
        #     elif len(basket1ball) == 3:
        #         basket1slot = [basket1ball[0]['color'], basket1ball[1]['color'], basket1ball[2]['color']]
        # else:
        #     basket1slot = [0, 0, 0]
        #
        # if len(basket2ball) > 0:
        #     if len(basket2ball) == 1:
        #         basket2slot = [basket2ball[0]['color'], 0, 0]
        #     elif len(basket2ball) == 2:
        #         basket2slot = [basket2ball[0]['color'], basket2ball[1]['color'], 0]
        #     elif len(basket2ball) == 3:
        #         basket2slot = [basket2ball[0]['color'], basket2ball[1]['color'], basket2ball[2]['color']]
        # else:
        #     basket2slot = [0, 0, 0]
        #
        # if len(basket3ball) > 0:
        #     if len(basket3ball) == 1:
        #         basket3slot = [basket3ball[0]['color'], 0, 0]
        #     elif len(basket3ball) == 2:
        #         basket3slot = [basket3ball[0]['color'], basket3ball[1]['color'], 0]
        #     elif len(basket3ball) == 3:
        #         basket3slot = [basket3ball[0]['color'], basket3ball[1]['color'], basket3ball[2]['color']]
        # else:
        #     basket3slot = [0, 0, 0]

        # print("1:")
        # print(basket1slot)
        # print("2:")
        # print(basket2slot)
        # print("3:")
        # print(basket3slot)

        if len(basket) > 0:
            obs.extend(basket_status)
            obs.extend(basket_full)
            print(obs)
            obs = obs + list(prev_actions)

            if len(obs) >= 40:

                action, _states = model.predict(obs)
                print("predict")
                print(action)

                if action == 0:
                    target0 += 1
                elif action == 1:
                    target1 += 1
                elif action == 2:
                    target2 += 1
                elif action == 3:
                    target3 += 1
                elif action == 4:
                    target4 += 1

        detect_time += 1
        var_clear()



    # cal_array.append = target0 / detect_time
    # cal_array.append = target1 / detect_time
    # cal_array.append = target2 / detect_time
    # cal_array.append = target3 / detect_time
    # cal_array.append = target4 / detect_time

    cal_array = [target0 / detect_time, target1 / detect_time, target2 / detect_time, target3 / detect_time, target4 / detect_time]
    print(cal_array)
    action = cal_array.index(max(cal_array))

    text_target = ("State: " + str(action))
    cv2.putText(img, text_target, (10, 10), font, 2, (0, 0, 255), 2)
    cv2.imshow("image", img)

    while action >= 0 and action <= 4:

        bg_removed, color_image = cam_start.realsense_start(pipeline, align, clipping_distance)

        print("action")
        print(action)
        basket_target = action
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

            # print(extLeft)
            # print(extRight)
            # print(extTop)

            cv2.circle(Wcrop_img, extRight, 1, (0, 255, 0), -1)
            cv2.circle(Wcrop_img, extLeft, 1, (255, 0, 0), -1)
            cv2.circle(Wcrop_img, extTop, 1, (0, 0, 255), -1)

            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                # print("CX: " + str(cx) + " CY: " + str(cy))

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
                state, pass_numberLine, w_counter = move_basket(white_area, basket_target, pass_numberLine, Wcontours,
                                                                extTop, state, w_counter)

        if state == 3:
            amount = np.sum(bg_removed)
            print(amount)
            if amount >= 14000000:
                state += 1
                value = [0xFF, 0x00, 0x00, 0x00, 0x00, 0x00]
                ser.write(serial.to_bytes(value))
                print("stop")

            else:
                move_command(cx)

        print("state")
        print(state)

        cv2.imshow('test', Wcrop_img)

        if cv2.waitKey(1) & 0xff == 27:
            break


    # y1 = basket[0]['y1']
    # y2 = basket[0]['y2']
    # x1 = basket[0]['x1']
    # x2 = basket[0]['x2']
    # basket_crop.append(img[y1:y2, x1:x2])
    # cv2.imshow("basket" + str(1), basket_crop[0])

    # for i in range(len(basket)):
    #     # print(basket[i]['x1'])
    #     # print(basket[i]['y1'])
    #     y1 = basket[i]['y1']
    #     y2 = basket[i]['y2']
    #     x1 = basket[i]['x1']
    #     x2 = basket[i]['x2']
    #     img_crop = img[y1:y2, x1:x2]
    #     img_crop = cv2.resize(img_crop,(150,200))
    #
    #     basket_crop.append(img_crop)

    # for i in range(len(basket)):
    #     images = np.hstack((basket_crop[i], )
    # if len(basket) > 0:
    #     if len(basket) == 1:
    #         img_crop = np.hstack(basket_crop[0])
    #     if len(basket) == 2:
    #         img_crop = np.hstack((basket_crop[0], basket_crop[1]))
    #     if len(basket) == 3:
    #         img_crop = np.hstack((basket_crop[0], basket_crop[1], basket_crop[2]))
    #     if len(basket) == 4:
    #         img_crop = np.hstack((basket_crop[0], basket_crop[1], basket_crop[2], basket_crop[3]))
    #     if len(basket) == 5:
    #         img_crop = np.hstack((basket_crop[0], basket_crop[1], basket_crop[2], basket_crop[3], basket_crop[4]))
    #
    #     cv2.imshow("crop", img_crop)


    # print("234")
    # bboxes1, class_ids1, scores1 = yd.detect(img_crop)
    #
    # for bbox1, class_id1, score1 in zip(bboxes1, class_ids1, scores1):
    #     print("bbox:", bbox1, "class id:", class_id1, "score:", score1)
    #     (x, y, x2, y2) = bbox1
    #     print("123")
    #
    #     if (score1 > 0.1 and class_id1 == 1) or (score1 > 0.1 and class_id1 == 3):
    #         cv2.rectangle(img_crop, (x, y), (x2, y2), (255, 0, 0), 2)
    #         item_center = [int((x + ((x2 - x) / 2))), int((y + ((y2 - y) / 2)))]
    #         cv2.circle(img_crop, (item_center[0], item_center[1]), 5, (0, 0, 0), -1)
    #
    #         # cv2.polylines(img, [seg], True, (0, 0, 255), 4)
    #         label = f'{CLASSES[class_id]} ({score:.2f})'
    #         # cv2.putText(img, str(class_id), (x, y - 10), font, 2, (0, 0, 255), 2)
    #         cv2.putText(img_crop, label, (x, y - 10), font, 2, (0, 0, 255), 2)

    newTime = time.time()
    FPS = str(int(1 / (newTime - startTime)))
    cv2.putText(img, FPS, (20, 50), font, 3, (255, 0, 0), 3)

    basket.clear()
    basket_crop.clear()
    ballstatus.clear()
    basket1ball.clear()
    basket2ball.clear()
    basket3ball.clear()
    basket4ball.clear()
    basket5ball.clear()
    basket_detail.clear()
    basket_status.clear()
    basket_full.clear()
    obs.clear()

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

    detect_time =0

    if cv2.waitKey(1) & 0xff == 27:
        break
# cam.release()
pipeline.stop()
cv2.destroyAllWindows()

