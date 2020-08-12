import numpy as np

class Figure:
    def __init__(self, id_, location, shape, color, contours=None):
        self.id = id_
        self.location = location
        self.contours = contours
        self.shape = shape
        self.color = color
    
    def __eq__(self, other):
        return np.linalg.norm(self.location - other.location) < 40