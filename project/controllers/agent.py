import numpy as np

class Agent:
    def __init__(self, id_, location):
        self.id = id_
        self.location = location
        self._direction = None
        self._target = None
    
    @property
    def direction(self):
        return self._direction
    @direction.setter
    def direction(self, direction):
        self._direction = direction
    @property
    def target(self):
        return self._target
    @target.setter
    def target(self, target):
        self._target = target
    
    def __eq__(self, other):
        return np.linalg.norm(self.location - other.location) < 40