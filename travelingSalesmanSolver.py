
import math
import random

""" This class represents a city in the TSP
 A city has an x and y coordinate
 These Nodes will represent the population in the genetic algorithm """


class CityNode:
    city_counter = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = "CITY " + str(self.city_counter)
        CityNode.city_counter += 1

    """ Users Pythagoras to determine the distance between this City node
    and another City node in a coordinate space """

    def distance_to(self, anotherCity):
        x_component = abs(self.x - anotherCity.x)
        y_component = abs(self.y - anotherCity.y)
        distance = math.sqrt((x_component**2)+(y_component**2))
        return distance

    """ For a clearer representation of the class """

    def __repr__(self):
        return "\n" + self.name + ": (" + str(self.x) + "," + str(self.y) + ")"


""" This class determines how adaptable (probability of surviving)
    an element is in regard to the overall population """


class Adaptability:
    def __init__(self, cities):
        self.cities = cities
        self.distance = 0
        self.adaptability = 0.0

    def determine_distance(self):
        if self.distance == 0:
            globalDistance = 0
            for i in range(0, len(self.cities)):
                origin = self.cities[i]
                destiny = None
                # If it is any other city
                if i+1 < len(self.cities):
                    destiny = self.cities[i+1]
                # If the last city has been visited
                else:
                    # Returns to the origin
                    # City in pos 0 is the origin city
                    destiny = self.cities[0]
                distance = origin.distance_to(destiny)
                globalDistance += distance
            self.distance = globalDistance
        return self.distance

    """ Calculates the adaptability attribute described in the genetic algorithm
    !!! REMEMBER: the lesser the distance, the better the solution """

    def determine_adaptability(self):
        if self.adaptability == 0:
            self.adaptability = 1/float(self.determine_distance())
        return self.adaptability


""" Creates the population described in the genetic algorithm. This gathers random tuples from the list
    to create the population. """


def create_single_route(cities):
    route = random.sample(cities, len(cities))
    return route


def determine_initial_population(size, cities):
    population = []
    for _ in range(0, size):
        population.append(create_single_route(cities))
    return population


""" Ranks the 'best' routes, which are the routes that will 'breed' in the Genetic Algorithm """


def determine_best_routes(population):
    results = {}
    for i in range(0, len(population)):
        results[i] = Adaptability(population[i]).determine_adaptability()
    """ The best routes are the ones with less distance.
        We use the key=lambda because we are creating an anonymous
        function to sort the list based on the first element on it """
    sorted_results = sorted(results.items(),
                            key=lambda x: x[1])
    return sorted_results


""" Selects the population members to be 'mated' for reproduction.
    In this case, the implemented process for selection
    is just selecting the top n (where n=elite_quantity)
    members in the adaptability rank """


def select_mating_pool(population, best_routes, elite_quantity):
    selected_members = []
    for i in range(elite_quantity):
        selected_members.append(best_routes[i][0])

    new_mating_pool = []
    for i in range(0, len(selected_members)):
        selected_member_index = selected_members[i]
        new_mating_pool.append(population[selected_member_index])

    return new_mating_pool


""" 'Create' a single child based on two parents. Implements a bit of randomness
    to simulate nature """


def produce_offspring(first_parent, second_parent):
    offspring = []
    offspring_1st_half = []
    offspring_2nd_half = []

    first_gene = int(random.random() * len(first_parent))
    second_gene = int(random.random() * len(first_parent))
    copied_set_start = min(first_gene, second_gene)
    copied_set_end = max(first_gene, second_gene)

    """ Copies a set (part) of random length from the first parent to the offpsring """
    for i in range(copied_set_start, copied_set_end):
        offspring_1st_half.append(first_parent[i])

    """ Fills the missing gaps in the offspring with the contents of the second parent """
    for chromosomes in second_parent:
        if chromosomes not in offspring_1st_half:
            offspring_2nd_half.append(chromosomes)
    offspring = offspring_1st_half+offspring_2nd_half

    return offspring


""" Breeds the population to create a new population with offsprings """


def breed_population(mating_pool, elite_quantity):
    offsprings = []
    new_pool = random.sample(mating_pool, len(mating_pool))

    for i in range(0, elite_quantity):
        offsprings.append(mating_pool[i])

    for i in range(0, len(mating_pool) - elite_quantity):
        offspring = produce_offspring(
            new_pool[i], new_pool[len(mating_pool-1-i)])

        offsprings.append(offspring)

    return offsprings


""" Simulates mutations of a single element in the list, to keep the general list still 'fresh'
    and to avoid an event called 'convergence' (results don't differ much) from happening early.
    Mutation happens on a certain probability (mutation_prob). The implementation of this mutation
    just switches the order of some random cities in the list. """


def mutate_single(single, mutation_prob):
    for original in range(len(single)):
        if(random.random() < mutation_prob):
            change_original = int(random.random()*len(single))
            city_placeholder1 = single[original]
            city_placeholder2 = single[change_original]
            single[original] = city_placeholder2
            single[change_original] = city_placeholder1
    return single


""" Sends all the population to the mutation function to see which are randomly mutated """


def mutate_population(population, mutation_prob):
    new_population = []

    for i in range(0, len(population)):
        new_mutation = mutate_single(population[i], mutation_prob)
        new_population.append(new_mutation)

    return new_population


""" Creates a new population based on the previous one """


def create_next_population(current_population, elite_quantity, mutation_prob):
    best_members = determine_best_routes(current_population)
    mating_pool = select_mating_pool(
        current_population, best_members, elite_quantity)
    offsprings = breed_population(mating_pool, elite_quantity)
    new_population = mutate_population(offsprings, mutation_prob)
    return new_population


""" Runs the genetic algorithm :) """


def genetic_algorithm(population, population_quantity, elite_quantity, mutation_prob, iterations):
    initial_population = determine_initial_population(
        population_quantity, population)
    dist_initial = determine_best_routes(initial_population)[0][1]
    print("Initial best distance: " + str(1/dist_initial))
    print("-----------------")

    best_route = determine_best_routes(initial_population)[0][0]
    print("Initial best solution for the Traveling Salesman: ",
          initial_population[best_route])

    new_population = initial_population
    for _ in range(0, iterations):
        new_population = create_next_population(
            new_population, elite_quantity, mutation_prob)
    print("-----------------")

    dist_final = determine_best_routes(new_population)[0][1]
    print("Final best distance: " + str(1/dist_final))
    print("-----------------")

    best_route = determine_best_routes(new_population)[0][0]
    print("Final best solution for the Traveling Salesman: ",
          new_population[best_route])


""" Randomly creates a list of 10 cities.
    Uncomment to TEST! """
""" random_cities = []
for i in range(0, 10):
    random_x = int(random.random()*50)
    random_y = int(random.random()*50)
    random_cities.append(CityNode(random_x, random_y)) """

""" Creates a list of 10 predetermined cities. """
cities = []
positions_x = [20, 30, 25, 15, 0, 32, 2, 3, 47, 11]
positions_y = [11, 47, 3, 2, 32, 0, 15, 25, 30, 20]
for i in range(10):
    cities.append(CityNode(positions_x[i], positions_y[i]))

""" Population, quantity of the population, elite quantity of chosen members, probability of mutation and iterations """
genetic_algorithm(cities, 100, 20, 0.5, 1000)

""" References:
* https://medium.com/@becmjo/genetic-algorithms-and-the-travelling-salesman-problem-d10d1daf96a1
* Suwannarongsri, Supaporn & Puangdownreong, Deacha. (2012). Solving traveling salesman problems via artificial intelligent search techniques. 137-141.
* https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
"""
