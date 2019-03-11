import kicker.control_environment as Env
import numpy as np
import tqdm
import random
from kicker.CONST_KICKER import *
from kicker.CONST_GAME_FIGURES import *

import matplotlib.pyplot as plt


def main():

    anz_angle = 91                          # Anzahl der random Startwinkel
    anz_pos = COURT_HEIGHT - 2*BALL_RADIUS

    total_episodes = 50000000 + 1
    episode_rewards = []
    env = Env.EnvironmentController()
    q_table = np.zeros([anz_angle * anz_pos, MAX_POS_FORWARD])
    alpha = 0.1
    gamma = 0.6
    epsilon = 1.0

    plt.ion()
    figure, ax = plt.subplots()
    lines, = ax.plot([], [], '-')

    ax.set_autoscaley_on(True)
    ax.grid()

    plot_rewards = []
    plot_episodes = []

    reward = 0.0

    for i in tqdm.tqdm(range(1, total_episodes)):
        state, _, _ = env.reset()
        done = False

        if random.uniform(0, 1) < epsilon:
            action = random.randint(0, 229)
        else:
            action = np.argmax(q_table[state])

        while not done:
            next_state, reward, done = env.step(action)
            # env.render()

        episode_rewards.append(reward)

        if np.mod(i, total_episodes / 1000) == 0:
            epsilon -= 0.001
            if epsilon <= 0.0:
                epsilon = 0.001

        old_value = q_table[state, action]
        # next_max = np.max(q_table[next_state])
        new_value = (1 - alpha) * old_value + alpha * reward  # (reward + gamma * next_max)
        q_table[state, action] = new_value

        if np.mod(i, 10000) == 0:
            print('Mean Reward: ', np.mean(episode_rewards), '  Games: ', i)

            # Plot
            plot_rewards.append(np.mean(episode_rewards))
            plot_episodes.append(i)

            lines.set_xdata(plot_episodes)
            lines.set_ydata(plot_rewards)

            ax.relim()
            ax.autoscale_view()

            figure.canvas.draw()
            figure.canvas.flush_events()

    # save Q-Table:
    np.save('/home/prock/data/q_table_07_01.npy', q_table)


if __name__ == '__main__':
    main()
