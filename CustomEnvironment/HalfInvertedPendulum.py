# HalfInvertedPendulum
#
# This file specifies the class for a half inverted pendulum. It is
# a custom environment and is similar to inverted_pendulum.py but
# reads from a different xml file
#
# Revision History:
# 05/18/18    Tim Liu    changed step() to _step to fix NotImplementedError
# 05/18/18    Tim Liu    changed  self.sim.data.qpos to self.model.data.qpos
# 05/18/18    Tim Liu    changed self.sim.data.qvel to self.model.data.qvel


import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env

class HalfInvertedPendulumEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        utils.EzPickle.__init__(self)
        mujoco_env.MujocoEnv.__init__(self, 'half_inverted_pendulum.xml', 2)

    def _step(self, a):
        reward = 1.0
        self.do_simulation(a, self.frame_skip)
        ob = self._get_obs()
        notdone = np.isfinite(ob).all() and (np.abs(ob[1]) <= .2)
        done = not notdone
        return ob, reward, done, {}

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(size=self.model.nq, low=-0.01, high=0.01)
        qvel = self.init_qvel + self.np_random.uniform(size=self.model.nv, low=-0.01, high=0.01)
        self.set_state(qpos, qvel)
        return self._get_obs()

    def _get_obs(self):
        return np.concatenate([self.model.data.qpos, self.model.data.qvel]).ravel()

    def viewer_setup(self):
        v = self.viewer
        v.cam.trackbodyid = 0
        v.cam.distance = self.model.stat.extent
