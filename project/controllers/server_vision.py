import cv2
import numpy as np

from . import Figure, Agent
from .image_processing import *


COLORS = ['blue', 'green', 'red']

class ServerVision:
    def __init__(self):
        self.figures = []
        self.agents = []

    def detect_object(self, img, shape:str=None, color:str=None):
        self.find_agents(img)
        self.find_objects(img)
        if shape is not None and color is not None:
            condition = list(map(lambda figure: (figure.shape == shape and figure.color == color), self.figures))
            self.set_agent_targets(condition)
        elif shape is not None:
            condition = list(map(lambda figure: (figure.shape == shape), self.figures))
            self.set_agent_targets(condition)
            pass
        else:
            condition = list(map(lambda figure: (figure.color == color), self.figures))
            self.set_agent_targets(condition)
            pass
        return self.create_path(img)
    
    def set_agent_targets(self, condition):
        figures = np.array(self.figures)[condition]
        locations = np.array(list(map(lambda figure: figure.location, figures)))
        for agent in self.agents:
            agent_loc = np.array(agent.location)
            index = np.argmin(np.linalg.norm(agent_loc - locations, axis=1))
            agent.target = figures[index]
    
    def create_path(self, img):
        angles = []
        for agent in self.agents:
            cv2.line(img, tuple(agent.location), tuple(agent.target.location), [0,0,0], 2)
            if agent.direction is not None:
                direction = agent.target.location - agent.location
                prod = np.sum(direction * agent.direction)
                angle = prod / (np.linalg.norm(direction) * np.linalg.norm(agent.direction))
                angle = np.arccos(angle)
                angle = np.rad2deg(angle)
                angles.append(angle)
        return angles
        

    def find_objects(self, img):
        for color in COLORS:
            mask = color_filter(img, encode_color(color))
            contours = find_contours(mask)
            locations = get_locations(contours)
            for location, contour in zip(locations, contours):
                shape = find_figure(contour)
                if self.figures:
                    id_ = self.figures[-1].id + 1
                else:
                    id_ = 0
                figure = Figure(id_, location, shape, color)
                if not figure in self.figures:
                    self.figures.append(figure)
                else:
                    self.figures[self.figures.index(figure)].location = location

        display_analysis(img, self.figures)
        pass
    def find_agents(self, img):
        mask = filter_yellow(img)
        contours = find_contours(mask)
        locations = get_locations(contours)
        for location in locations:
            if self.agents:
                id_ = self.agents[-1].id + 1
            else:
                id_ = 0
            agent = Agent(id_, location)
            if not agent in self.agents:
                self.agents.append(agent)
            else:
                agent = self.agents[self.agents.index(agent)]
                direction = location - agent.location
                agent.location = location
                agent.direction = direction
        display_agent(img, self.agents)