import gym
import random
import numpy as np
from skimage.transform import resize
from skimage.color import rgb2gray


class Environment(object):

    def __init__(self, config):
        self.env = gym.make(config.env_name)

        screen_width, screen_height, self.action_repeat, self.random_start = \
            config.screen_width, config.screen_height, config.action_repeat, config.random_start

        self.display = config.display
        self.dims = (screen_width, screen_height)

        self._screen = None
        self.reward = 0
        self.terminal = True

    def new_game(self, from_random_game=False):
        if self.lives == 0:
            self._screen = self.env.reset()
        self._step(0)
        self.render()
        return self.screen, 0, 0, self.terminal

    def new_random_game(self):
        self.new_game(True)
        for _ in range(random.randint(0, self.random_start - 1)):
            self._step(0)
        self.render()
        return self.screen, 0, 0, self.terminal

    def _step(self, action):
        self._screen, self.reward, self.terminal, _ = self.env.step(action)

    def _random_step(self):
        action = self.env.action_space.sample()
        self._step(action)

    @property
    def screen(self):
        return resize(rgb2gray(self._screen) / 255.0, self.dims)

    @property
    def action_size(self):
        return self.env.action_space.n

    @property
    def lives(self):
        return self.env.ale.lives()

    @property
    def state(self):
        return self.screen, self.reward, self.terminal

    def render(self):
        if self.display:
            self.env.render()

    def after_act(self, action):
        self.render()


class GymEnvironment(Environment):

    def __init__(self, config):
        super(GymEnvironment, self).__init__(config)

    def act(self, action, is_training=True):
        self._step(action)

        self.after_act(action)
        return self.state
