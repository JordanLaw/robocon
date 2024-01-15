from stable_baselines3 import PPO
from stable_baselines3 import A2C
import os
from snakeenv import SnekEnv
from environment_blue_ball_first import CustomEnv
import time

models_dir = f"models/{int(time.time())}/"
logdir = f"logs/{int(time.time())}/"

if not os.path.exists(models_dir):
	os.makedirs(models_dir)

if not os.path.exists(logdir):
	os.makedirs(logdir)

# env = SnekEnv()
env = CustomEnv()
env.reset()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=logdir)
# model = PPO.load("models/1698772742/110000.zip", env)

TIMESTEPS = 2048
iters = 0
while True:
	iters += 1
	model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name=f"PPO")
	model.save("models/20231102-ver1 (blue ball first).zip")