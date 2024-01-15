import gym
from stable_baselines3 import PPO
from stable_baselines3 import A2C
from environment import CustomEnv
import numpy as np
import cv2
import draw_boxes
import time
from collections import deque

ai_action_check = 0
human_action_check = 0
done = 0
red_silo = 0
blue_silo = 0
font = cv2.FONT_HERSHEY_SIMPLEX
basketFull = 0

basket1 = [100, 300, 0], [100, 200, 0], [100, 100, 0]
basket2 = [250, 300, 0], [250, 200, 0], [250, 100, 0]
basket3 = [400, 300, 0], [400, 200, 0], [400, 100, 0]
basket4 = [550, 300, 0], [550, 200, 0], [550, 100, 0]
basket5 = [700, 300, 0], [700, 200, 0], [700, 100, 0]

basket1slot1 = basket1[0][2]
basket1slot2 = basket1[1][2]
basket1slot3 = basket1[2][2]

basket2slot1 = basket2[0][2]
basket2slot2 = basket2[1][2]
basket2slot3 = basket2[2][2]

basket3slot1 = basket3[0][2]
basket3slot2 = basket3[1][2]
basket3slot3 = basket3[2][2]

basket4slot1 = basket4[0][2]
basket4slot2 = basket4[1][2]
basket4slot3 = basket4[2][2]

basket5slot1 = basket5[0][2]
basket5slot2 = basket5[1][2]
basket5slot3 = basket5[2][2]

basket1Full = 0
basket2Full = 0
basket3Full = 0
basket4Full = 0
basket5Full = 0

env = CustomEnv()

model = PPO.load("models/20231102-ver4 (red ball first)_final.zip")

prev_actions = deque(maxlen=20)  # however long we aspire the snake to be
for i in range(20):
    prev_actions.append(-1)

obs = [basket1slot1,basket1slot2,basket1slot3,
       basket2slot1,basket2slot2,basket2slot3,
       basket3slot1,basket3slot2,basket3slot3,
       basket4slot1,basket4slot2,basket4slot3,
       basket5slot1,basket5slot2,basket5slot3,
       basket1Full,basket2Full,basket3Full,basket4Full,basket5Full] + list(prev_actions)

img = np.zeros((500, 900, 3), dtype='uint8')
draw_boxes.draw(img)

# print(obs)
while True:
    while done == 0:
        cv2.imshow('test', img)
        cv2.waitKey(1)

        while ai_action_check == 0:
            action, _states = model.predict(obs)
            prev_actions.append(action)

            print(obs)
            print(action)

            if action == 0 and basket1slot3 == 0:
                if basket1slot1 == 0:
                    cv2.circle(img, (basket1[0][0] + 50, basket1[0][1] + 50), 20, (0, 0, 255), -1)
                    basket1slot1 = 1
                    obs[0] = basket1slot1
                    ai_action_check = 1
                elif basket1slot2 == 0:
                    cv2.circle(img, (basket1[1][0] + 50, basket1[1][1] + 50), 20, (0, 0, 255), -1)
                    basket1slot2 = 1
                    obs[1] = basket1slot2
                    ai_action_check = 1
                elif basket1slot3 == 0:
                    cv2.circle(img,(basket1[2][0] + 50, basket1[2][1] + 50), 20, (0, 0, 255), -1)
                    basket1slot3 = 1
                    obs[2] = basket1slot3
                    basketFull += 1
                    ai_action_check = 1
                    basket1Full = 1
                    obs[15] = basket1Full
                    if basket1slot1 == 1 or basket1slot2 == 1:
                        red_silo += 1

            elif action == 1 and basket2slot3 == 0:
                if basket2slot1 == 0:
                    cv2.circle(img,(basket2[0][0] + 50, basket2[0][1] + 50), 20, (0, 0, 255), -1)
                    basket2slot1 = 1
                    obs[3] = basket2slot1
                    ai_action_check = 1
                elif basket2slot2 == 0:
                    cv2.circle(img,(basket2[1][0] + 50, basket2[1][1] + 50), 20, (0, 0, 255), -1)
                    basket2slot2 = 1
                    obs[4] = basket2slot2
                    ai_action_check = 1
                elif basket2slot3 == 0:
                    cv2.circle(img,(basket2[2][0] + 50, basket2[2][1] + 50), 20, (0, 0, 255), -1)
                    basket2slot3 = 1
                    obs[5] = basket2slot3
                    ai_action_check = 1
                    basketFull += 1
                    basket2Full = 1
                    obs[16] = basket2Full
                    if basket2slot1 == 1 or basket2slot2 == 1:
                        red_silo += 1

            elif action == 2 and basket3slot3 == 0:
                if basket3slot1 == 0:
                    cv2.circle(img,(basket3[0][0] + 50, basket3[0][1] + 50), 20, (0, 0, 255), -1)
                    basket3slot1 = 1
                    obs[6] = basket3slot1
                    ai_action_check = 1
                elif basket3slot2 == 0:
                    cv2.circle(img,(basket3[1][0] + 50, basket3[1][1] + 50), 20, (0, 0, 255), -1)
                    basket3slot2 = 1
                    obs[7] = basket3slot2
                    ai_action_check = 1
                elif basket3slot3 == 0:
                    cv2.circle(img,(basket3[2][0] + 50, basket3[2][1] + 50), 20, (0, 0, 255), -1)
                    basket3slot3 = 1
                    obs[8] = basket3slot3
                    ai_action_check = 1
                    basketFull += 1
                    basket3Full = 1
                    obs[17] = basket3Full
                    if basket3slot1 == 1 or basket3slot2 == 1:
                        red_silo += 1

            elif action == 3 and basket4slot3 == 0:
                if basket4slot1 == 0:
                    cv2.circle(img,(basket4[0][0] + 50, basket4[0][1] + 50), 20, (0, 0, 255), -1)
                    basket4slot1 = 1
                    obs[9] = basket4slot1
                    ai_action_check = 1
                elif basket4slot2 == 0:
                    cv2.circle(img,(basket4[1][0] + 50, basket4[1][1] + 50), 20, (0, 0, 255), -1)
                    basket4slot2 = 1
                    obs[10] = basket4slot2
                    ai_action_check = 1
                elif basket4slot3 == 0:
                    cv2.circle(img,(basket4[2][0] + 50, basket4[2][1] + 50), 20, (0, 0, 255), -1)
                    basket4slot3 = 1
                    obs[11] = basket4slot3
                    ai_action_check = 1
                    basketFull += 1
                    basket4Full = 1
                    obs[18] = basket4Full
                    if basket4slot1 == 1 or basket4slot2 == 1:
                        red_silo += 1

            elif action == 4 and basket5slot3 == 0:
                if basket5slot1 == 0:
                    cv2.circle(img,(basket5[0][0] + 50, basket5[0][1] + 50), 20, (0, 0, 255), -1)
                    basket5slot1 = 1
                    obs[12] = basket5slot1
                    ai_action_check = 1
                elif basket5slot2 == 0:
                    cv2.circle(img,(basket5[1][0] + 50, basket5[1][1] + 50), 20, (0, 0, 255), -1)
                    basket5slot2 = 1
                    obs[13] = basket5slot2
                    ai_action_check = 1
                elif basket5slot3 == 0:
                    cv2.circle(img,(basket5[2][0] + 50, basket5[2][1] + 50), 20, (0, 0, 255), -1)
                    basket5slot3 = 1
                    obs[14] = basket5slot3
                    ai_action_check = 1
                    basketFull += 1
                    basket5Full = 1
                    obs[19] = basket5Full
                    if basket5slot1 == 1 or basket5slot2 == 1:
                        red_silo += 1

            cv2.imshow('test', img)
            cv2.waitKey(1)

        print(obs)
        ai_action_check = 0

        # t_end = time.time() + 0.05
        # k = -1
        # while time.time() < t_end:
        #     if k == -1:
        #         k = cv2.waitKey(1)
        #     else:
        #         continue

        print("1: basket: " + str(basketFull) + " red: " + str(red_silo) + " blue: " + str(blue_silo))

        if basketFull == 5:
            human_action_check = 1
        elif red_silo == 3:
            human_action_check = 1
        else:
            k = cv2.waitKey(0)

        while human_action_check == 0:
            if k == ord('1') and basket1slot3 == 0:
                if basket1slot1 == 0:
                    cv2.circle(img,(basket1[0][0] + 50, basket1[0][1] + 50), 20, (255, 0, 0), -1)
                    basket1slot1 = 2
                    obs[0] = basket1slot1
                    human_action_check = 1
                elif basket1slot2 == 0:
                    cv2.circle(img,(basket1[1][0] + 50, basket1[1][1] + 50), 20, (255, 0, 0), -1)
                    basket1slot2 = 2
                    obs[1] = basket1slot2
                    human_action_check = 1
                elif basket1slot3 == 0:
                    cv2.circle(img,(basket1[2][0] + 50, basket1[2][1] + 50), 20, (255, 0, 0), -1)
                    basket1slot3 = 2
                    obs[2] = basket1slot3
                    human_action_check = 1
                    basketFull += 1
                    basket1Full = 1
                    obs[15] = basket1Full
                    if basket1slot1 == 2 or basket1slot2 == 2:
                        blue_silo += 1
                else:
                    print("error")

            elif k == ord('2') and basket2slot3 == 0:
                if basket2slot1 == 0:
                    cv2.circle(img,(basket2[0][0] + 50, basket2[0][1] + 50), 20, (255, 0, 0), -1)
                    basket2slot1 = 2
                    obs[3] = basket2slot1
                    human_action_check = 1
                elif basket2slot2 == 0:
                    cv2.circle(img,(basket2[1][0] + 50, basket2[1][1] + 50), 20, (255, 0, 0), -1)
                    basket2slot2 = 2
                    obs[4] = basket2slot2
                    human_action_check = 1
                elif basket2slot3 == 0:
                    cv2.circle(img,(basket2[2][0] + 50, basket2[2][1] + 50), 20, (255, 0, 0), -1)
                    basket2slot3 = 2
                    obs[5] = basket2slot3
                    human_action_check = 1
                    basketFull += 1
                    basket2Full = 1
                    obs[16] = basket2Full
                    if basket2slot1 == 2 or basket2slot2 == 2:
                        blue_silo += 1
                else:
                    print("error")

            elif k == ord('3') and basket3slot3 == 0:
                if basket3slot1 == 0:
                    cv2.circle(img,(basket3[0][0] + 50, basket3[0][1] + 50), 20, (255, 0, 0), -1)
                    basket3slot1 = 2
                    obs[6] = basket3slot1
                    human_action_check = 1
                elif basket3slot2 == 0:
                    cv2.circle(img,(basket3[1][0] + 50, basket3[1][1] + 50), 20, (255, 0, 0), -1)
                    basket3slot2 = 2
                    obs[7] = basket3slot2
                    human_action_check = 1
                elif basket3slot3 == 0:
                    cv2.circle(img,(basket3[2][0] + 50, basket3[2][1] + 50), 20, (255, 0, 0), -1)
                    basket3slot3 = 2
                    obs[8] = basket3slot3
                    human_action_check = 1
                    basketFull += 1
                    basket3Full = 1
                    obs[17] = basket3Full
                    if basket3slot1 == 2 or basket3slot2 == 2:
                        blue_silo += 1
                else:
                    print("error")

            elif k == ord('4') and basket4slot3 == 0:
                if basket4slot1 == 0:
                    cv2.circle(img,(basket4[0][0] + 50, basket4[0][1] + 50), 20, (255, 0, 0), -1)
                    basket4slot1 = 2
                    obs[9] = basket4slot1
                    human_action_check = 1
                elif basket4slot2 == 0:
                    cv2.circle(img,(basket4[1][0] + 50, basket4[1][1] + 50), 20, (255, 0, 0), -1)
                    basket4slot2 = 2
                    obs[10] = basket4slot2
                    human_action_check = 1
                elif basket4slot3 == 0:
                    cv2.circle(img,(basket4[2][0] + 50, basket4[2][1] + 50), 20, (255, 0, 0), -1)
                    basket4slot3 = 2
                    obs[11] = basket4slot3
                    human_action_check = 1
                    basketFull += 1
                    basket4Full = 1
                    obs[18] = basket4Full
                    if basket4slot1 == 2 or basket4slot2 == 2:
                        blue_silo += 1
                else:
                    print("error")

            elif k == ord('5') and basket5slot3 == 0:
                if basket5slot1 == 0:
                    cv2.circle(img,(basket5[0][0] + 50, basket5[0][1] + 50), 20, (255, 0, 0), -1)
                    basket5slot1 = 2
                    obs[12] = basket5slot1
                    human_action_check = 1
                elif basket5slot2 == 0:
                    cv2.circle(img,(basket5[1][0] + 50, basket5[1][1] + 50), 20, (255, 0, 0), -1)
                    basket5slot2 = 2
                    obs[13] = basket5slot2
                    human_action_check = 1
                elif basket5slot3 == 0:
                    cv2.circle(img,(basket5[2][0] + 50, basket5[2][1] + 50), 20, (255, 0, 0), -1)
                    basket5slot3 = 2
                    obs[14] = basket5slot3
                    human_action_check = 1
                    basketFull += 1
                    basket5Full = 1
                    obs[19] = basket4Full
                    if basket5slot1 == 2 or basket5slot2 == 2:
                        blue_silo += 1
                else:
                    print("error")

            elif k == ord('q'):
                done = 1
                human_action_check = 1

            else:
                print("error")
                k = cv2.waitKey(0)

            cv2.imshow('test', img)
            cv2.waitKey(1)

        human_action_check = 0
        print(obs)

        print("2: basket: " + str(basketFull) + " red: " + str(red_silo) + " blue: " + str(blue_silo))


        if red_silo == 3:
            img = np.zeros((500, 900, 3), dtype='uint8')
            cv2.putText(img, "red win", (140,250), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("test", img)
            cv2.waitKey(1)
            done = 1

        if blue_silo == 3:
            img = np.zeros((500, 900, 3), dtype='uint8')
            cv2.putText(img, "blue win", (140,250), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("test", img)
            cv2.waitKey(1)
            done = 1

        if basketFull == 5 and red_silo < 3 and blue_silo < 3:
            img = np.zeros((500, 900, 3), dtype='uint8')
            cv2.putText(img, "Tie", (140,250), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.waitKey(1)
            done = 1

    if done == 1:
        cv2.putText(img, "Retry? press r. If not, press q", (140, 350), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("test", img)
        cv2.waitKey(1)

    if done == 1:
        k = cv2.waitKey(0)

        if k == ord('r'):
            done = 0
            img = np.zeros((500, 900, 3), dtype='uint8')
            draw_boxes.draw(img)
            ai_action_check = 0
            human_action_check = 0
            red_silo = 0
            blue_silo = 0
            basketFull = 0

            basket1slot1 = 0
            basket1slot2 = 0
            basket1slot3 = 0

            basket2slot1 = 0
            basket2slot2 = 0
            basket2slot3 = 0

            basket3slot1 = 0
            basket3slot2 = 0
            basket3slot3 = 0

            basket4slot1 = 0
            basket4slot2 = 0
            basket4slot3 = 0

            basket5slot1 = 0
            basket5slot2 = 0
            basket5slot3 = 0

            basket1Full = 0
            basket2Full = 0
            basket3Full = 0
            basket4Full = 0
            basket5Full = 0

            prev_actions = deque(maxlen=20)  # however long we aspire the snake to be
            for i in range(20):
                prev_actions.append(-1)

            obs = [basket1slot1, basket1slot2, basket1slot3,
                   basket2slot1, basket2slot2, basket2slot3,
                   basket3slot1, basket3slot2, basket3slot3,
                   basket4slot1, basket4slot2, basket4slot3,
                   basket5slot1, basket5slot2, basket5slot3,
                   basket1Full, basket2Full, basket3Full, basket4Full, basket5Full] + list(prev_actions)

        elif k == ord('q'):
            break

cv2.destroyAllWindows()

    # obs, rewards, dones, info = env.step(action)



