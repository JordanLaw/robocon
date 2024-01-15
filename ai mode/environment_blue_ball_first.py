import cv2
import numpy as np
import time
import action_AI
import gym
import draw_boxes
from gym import spaces
from collections import deque
import random


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self):
        super(CustomEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(5)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=0, high=4, shape=(40,), dtype=np.int32)

    def step(self, action):
        self.prev_actions.append(action)
        cv2.imshow('test', self.img)
        cv2.waitKey(1)
        # self.img = np.zeros((500,900,3),dtype='uint8')
        # draw_boxes.draw(self.img)

        AI_action = action

        while self.action_check == 0:
            if AI_action == 0 and self.basketFull[0] == 0:
                self.img, self.playerTurn, self.basket1, self.basketFull[0], self.score, self.red_silo, self.blue_silo\
                    = action_AI.basket_store(self.img, self.playerTurn, self.basket1, self.score, self.red_silo, self.blue_silo)
                self.action_check = 1
            elif AI_action == 1 and self.basketFull[1] == 0:
                self.img, self.playerTurn, self.basket2, self.basketFull[1], self.score, self.red_silo, self.blue_silo \
                    = action_AI.basket_store(self.img, self.playerTurn, self.basket2, self.score, self.red_silo, self.blue_silo)
                self.action_check = 1
            elif AI_action == 2 and self.basketFull[2] == 0:
                self.img, self.playerTurn, self.basket3, self.basketFull[2], self.score, self.red_silo, self.blue_silo \
                    = action_AI.basket_store(self.img, self.playerTurn, self.basket3, self.score, self.red_silo, self.blue_silo)
                self.action_check = 1
            elif AI_action == 3 and self.basketFull[3] == 0:
                self.img, self.playerTurn, self.basket4, self.basketFull[3], self.score, self.red_silo, self.blue_silo \
                    = action_AI.basket_store(self.img, self.playerTurn, self.basket4, self.score, self.red_silo, self.blue_silo)
                self.action_check = 1
            elif AI_action == 4 and self.basketFull[4] == 0:
                self.img, self.playerTurn, self.basket5, self.basketFull[4], self.score, self.red_silo, self.blue_silo \
                    = action_AI.basket_store(self.img, self.playerTurn, self.basket5, self.score, self.red_silo, self.blue_silo)
                self.action_check = 1
            elif self.prev_action_check == action:
                self.score -= 10
                self.action_check += 1
                self.random_action_check = 1
            elif self.action_check >= 5:
                self.score -= 10
                self.done = True
            else:
                self.score -= 10
                self.action_check += 1
                self.random_action_check = 1

        self.action_check = 0
        self.prev_action_check = action

        while self.random_action_check == 0 and self.done == False:

            if self.basketFull[0] == 1 and self.basketFull[1] == 1 and self.basketFull[2] == 1 and self.basketFull[3] \
                    == 1 and self.basketFull[4] == 1:
                break

            self.random_list = [0,1,2,3,4]

            if self.basketFull [0] == 1:
                self.random_list.remove(0)
            if self.basketFull [1] == 1:
                self.random_list.remove(1)
            if self.basketFull [2] == 1:
                self.random_list.remove(2)
            if self.basketFull [3] == 1:
                self.random_list.remove(3)
            if self.basketFull [4] == 1:
                self.random_list.remove(4)

            self.random_action = random.choice(self.random_list)

            if self.random_action == 0 and self.basketFull[0] == 0:
                self.img, self.playerTurn, self.basket1, self.basketFull[0], self.score, self.red_silo, self.blue_silo \
                    = action_AI.basket_store(self.img, self.playerTurn, self.basket1, self.score, self.red_silo, self.blue_silo)
                self.random_action_check = 1
            elif self.random_action == 1 and self.basketFull[1] == 0:
                self.img, self.playerTurn, self.basket2, self.basketFull[1], self.score, self.red_silo, self.blue_silo = action_AI.basket_store(
                    self.img, self.playerTurn, self.basket2, self.score, self.red_silo, self.blue_silo)
                self.random_action_check = 1
            elif self.random_action == 2 and self.basketFull[2] == 0:
                self.img, self.playerTurn, self.basket3, self.basketFull[2], self.score, self.red_silo, self.blue_silo = action_AI.basket_store(
                    self.img, self.playerTurn, self.basket3, self.score, self.red_silo, self.blue_silo)
                self.random_action_check = 1
            elif self.random_action == 3 and self.basketFull[3] == 0:
                self.img, self.playerTurn, self.basket4, self.basketFull[3], self.score, self.red_silo, self.blue_silo = action_AI.basket_store(
                    self.img, self.playerTurn, self.basket4, self.score, self.red_silo, self.blue_silo)
                self.random_action_check = 1
            elif self.random_action == 4 and self.basketFull[4] == 0:
                self.img, self.playerTurn, self.basket5, self.basketFull[4], self.score, self.red_silo, self.blue_silo = action_AI.basket_store(
                    self.img, self.playerTurn, self.basket5, self.score, self.red_silo, self.blue_silo)
                self.random_action_check = 1

        self.random_action_check = 0

        if self.red_silo == 3:
            self.score += 50
            self.done = True

        if self.blue_silo == 3:
            self.score -= 50
            self.done = True

        if self.basketFull[0] == 1 and self.basketFull[1] == 1 and self.basketFull[2] == 1 and self.basketFull[3] == 1 and self.basketFull[4] == 1:
            self.score += 5
            self.done = True

        self.total_reward = self.score  # default length is 3
        self.reward = self.total_reward - self.prev_reward
        self.prev_reward = self.total_reward

        info = {}

        basket1slot1 = self.basket1[0][2]
        basket1slot2 = self.basket1[1][2]
        basket1slot3 = self.basket1[2][2]

        basket2slot1 = self.basket2[0][2]
        basket2slot2 = self.basket2[1][2]
        basket2slot3 = self.basket2[2][2]

        basket3slot1 = self.basket3[0][2]
        basket3slot2 = self.basket3[1][2]
        basket3slot3 = self.basket3[2][2]

        basket4slot1 = self.basket4[0][2]
        basket4slot2 = self.basket4[1][2]
        basket4slot3 = self.basket4[2][2]

        basket5slot1 = self.basket5[0][2]
        basket5slot2 = self.basket5[1][2]
        basket5slot3 = self.basket5[2][2]

        basket1Full = self.basketFull[0]
        basket2Full = self.basketFull[1]
        basket3Full = self.basketFull[2]
        basket4Full = self.basketFull[3]
        basket5Full = self.basketFull[4]

        observation = [basket1slot1, basket1slot2, basket1slot3,
                       basket2slot1, basket2slot2, basket2slot3,
                       basket3slot1, basket3slot2, basket3slot3,
                       basket4slot1, basket4slot2, basket4slot3,
                       basket5slot1, basket5slot2, basket5slot3,
                       basket1Full, basket2Full, basket3Full, basket4Full, basket5Full] + list(self.prev_actions)

        observation = np.array(observation)

        cv2.imshow('test', self.img)
        cv2.waitKey(1)

        return observation, self.reward, self.done, info

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def reset(self):
        self.img = np.zeros((500,900,3),dtype='uint8')
        draw_boxes.draw(self.img)

        self.basket1 = [100, 300, 0], [100, 200, 0], [100, 100, 0]
        self.basket2 = [250, 300, 0], [250, 200, 0], [250, 100, 0]
        self.basket3 = [400, 300, 0], [400, 200, 0], [400, 100, 0]
        self.basket4 = [550, 300, 0], [550, 200, 0], [550, 100, 0]
        self.basket5 = [700, 300, 0], [700, 200, 0], [700, 100, 0]

        blue_first = random.randint(0, 4)

        if blue_first == 0:
            self.basket1[0][2] = 2
            cv2.circle(self.img, (self.basket1[0][0] + 50, self.basket1[0][1] + 50), 20, (0, 0, 255), -1)
        elif blue_first == 1:
            self.basket2[0][2] = 2
            cv2.circle(self.img, (self.basket2[0][0] + 50, self.basket2[0][1] + 50), 20, (0, 0, 255), -1)
        elif blue_first == 2:
            self.basket3[0][2] = 2
            cv2.circle(self.img, (self.basket3[0][0] + 50, self.basket3[0][1] + 50), 20, (0, 0, 255), -1)
        elif blue_first == 3:
            self.basket4[0][2] = 2
            cv2.circle(self.img, (self.basket4[0][0] + 50, self.basket4[0][1] + 50), 20, (0, 0, 255), -1)
        elif blue_first == 4:
            self.basket5[0][2] = 2
            cv2.circle(self.img, (self.basket5[0][0] + 50, self.basket5[0][1] + 50), 20, (0, 0, 255), -1)



        self.basketFull = [0, 0, 0, 0, 0]

        self.score = 0
        self.playerTurn = 1
        self.action_check = 0
        self.random_action_check = 0
        self.red_silo = 0
        self.blue_silo = 0
        self.repeat_time = 0
        self.prev_action_check = 0

        basket1Full = self.basketFull[0]
        basket2Full = self.basketFull[1]
        basket3Full = self.basketFull[2]
        basket4Full = self.basketFull[3]
        basket5Full = self.basketFull[4]

        basket1slot1 = self.basket1[0][2]
        basket1slot2 = self.basket1[1][2]
        basket1slot3 = self.basket1[2][2]

        basket2slot1 = self.basket2[0][2]
        basket2slot2 = self.basket2[1][2]
        basket2slot3 = self.basket2[2][2]

        basket3slot1 = self.basket3[0][2]
        basket3slot2 = self.basket3[1][2]
        basket3slot3 = self.basket3[2][2]

        basket4slot1 = self.basket4[0][2]
        basket4slot2 = self.basket4[1][2]
        basket4slot3 = self.basket4[2][2]

        basket5slot1 = self.basket5[0][2]
        basket5slot2 = self.basket5[1][2]
        basket5slot3 = self.basket5[2][2]

        self.prev_reward = 0

        self.done = False

        self.prev_actions = deque(maxlen=20)  # however long we aspire the snake to be
        for i in range(20):
            self.prev_actions.append(-1)

        observation = [basket1slot1, basket1slot2, basket1slot3,
                       basket2slot1, basket2slot2, basket2slot3,
                       basket3slot1, basket3slot2, basket3slot3,
                       basket4slot1, basket4slot2, basket4slot3,
                       basket5slot1, basket5slot2, basket5slot3,
                       basket1Full, basket2Full, basket3Full, basket4Full, basket5Full] + list(self.prev_actions)

        observation = np.array(observation, dtype=np.int32)

        return observation