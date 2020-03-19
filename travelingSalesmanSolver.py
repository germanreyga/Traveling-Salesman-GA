# Requires some SciPy libraries
import math

# This Node represents a city in the TSP
# A city has an x and y coordinate
# These Nodes will represent the population in the genetic algorithm


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Users Pythagoras to determine the distance between this Node
    # and another Node in a coordinate space
    def distance(self, anotherCity):
        x_component = abs(self.x - anotherCity.x)
        y_component = abs(self.y - anotherCity.y)
        distance = math.sqrt((x_component**2)+(y_component**2))
        return distance

    def __repr__(self):
        return "(" + self.x + "," + self.y + ")"
