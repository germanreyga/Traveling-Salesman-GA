# Requires some SciPy libraries
import math

# This Node represents a city in the TSP
# A city has an x and y coordinate
# These Nodes will represent the population in the genetic algorithm


class CityNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Users Pythagoras to determine the distance between this City node
    # and another City node in a coordinate space
    def distance_to(self, anotherCity):
        x_component = abs(self.x - anotherCity.x)
        y_component = abs(self.y - anotherCity.y)
        distance = math.sqrt((x_component**2)+(y_component**2))
        return distance

    # For a better representation
    def __repr__(self):
        return "(" + self.x + "," + self.y + ")"


class Fitness:
    def __init__(self, cities):
        self.cities = cities
        self.distance = 0
        self.fitness = 0.0

    def cities_distance(self):
        if self.distance == 0:
            globalDistance = 0
            for i in range(0, len(self.cities)):
                origin = self.cities[i]
                destiny = None
                # If it is any other city
                if i+1 < len(self.cities):
                    destiny = self.cities[i+1]
                # If the last city has been visited
                elif i+1 >= len(self.cities):
                    # Returns to the origin
                    # City in pos 0 is the origin city
                    destiny = self.cities[0]
                distance = origin.distance_to(destiny)
                globalDistance += distance
            self.distance = globalDistance
        return self.distance

    # Calculates the fitness attribute of the genetic algorithm
    def cities_fitness(self):
        if self.fitness == 0:
            self.fitness = 1/self.cities_distance()
        return self.fitness
