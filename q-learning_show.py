import kicker.control_environment as Env
import numpy as np
from kicker.CONST_KICKER import *
from kicker.CONST_GAME_FIGURES import *
import pygame
import matplotlib.pyplot as plt
from kicker.CONST_KICKER import *
from kicker.CONST_GAME_FIGURES import *


def main():

    clock = pygame.time.Clock()

    total_episodes = 10 + 1
    env = Env.EnvironmentController()

    # save Q-Table:
    q_table = np.load('/home/prock/ProCK/data/q_table_07_01.npy')

    for i in range(0, COURT_HEIGHT - 2*BALL_RADIUS, 10):
        plt.imshow(np.transpose(q_table[i*91:i*91+10*90, :]), origin='lower')
       # plt.show()

    # print(np.max(q_table))
    episode_rewards = []
    reward = 0.0

    for i in range(1, total_episodes):
        state, _, _ = env.reset()
        done = False

        action = np.argmax(q_table[state])

        while not done:
            next_state, reward, done = env.step(action)
            env.render()
            clock.tick_busy_loop(80)

        episode_rewards.append(reward)

    print('Mean Reward: ', np.mean(episode_rewards), '  Games: ', total_episodes)


if __name__ == '__main__':
    main()
