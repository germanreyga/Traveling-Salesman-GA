
import math
import random
import operator
"""
 This Node represents a city in the TSP
 A city has an x and y coordinate
 These Nodes will represent the population in the genetic algorithm
"""


class CityNode:
    city_counter = 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.name = "CITY " + str(self.city_counter)
        CityNode.city_counter += 1

    cityCounter = 1
    # Users Pythagoras to determine the distance between this City node
    # and another City node in a coordinate space

    def distance_to(self, anotherCity):
        x_component = abs(self.x - anotherCity.x)
        y_component = abs(self.y - anotherCity.y)
        distance = math.sqrt((x_component**2)+(y_component**2))
        return distance

    # For a better representation
    def __repr__(self):
        return "\n" + self.name + ": (" + str(self.x) + "," + str(self.y) + ")"


class Fitness:
    def __init__(self, cities):
        self.cities = cities
        self.distance = 0
        self.fitness = 0.0

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

    """ Calculates the fitness attribute described in the genetic algorithm
    !!! REMEMBER: the lesser the distance, the better the solution """

    def determine_fitness(self):
        if self.fitness == 0:
            self.fitness = 1/float(self.determine_distance())
        return self.fitness


""" Creates the population described in the genetic algorithm """


def create_single_route(cities):
    route = random.sample(cities, len(cities))
    return route


def determine_initial_population(size, cities):
    population = []
    for _ in range(0, size):
        population.append(create_single_route(cities))
    return population


""" Ranks the 'fittest' routes, which are the routes that will 'breed' in the GA """


def determine_fittest_routes(population):
    results = {}
    for i in range(0, len(population)):
        results[i] = Fitness(population[i]).determine_fitness()
    # The best routes are the ones with less distance
    # sortedResults = sorted(results)
    sorted_results = sorted(results.items(),
                            key=operator.itemgetter(1))
    return sorted_results


""" Selects the population members to be 'mated' for reproduction.
    In this case, the implemented process for selection
    is just selecting the better routes in the fit rank """


def select_mating_pool(population, fittest_routes, elite_quantity):
    selected_members = []
    for i in range(elite_quantity):
        selected_members.append(fittest_routes[i][0])

    new_mating_pool = []
    for i in range(0, len(selected_members)):
        selected_member_index = selected_members[i]
        new_mating_pool.append(population[selected_member_index])

    return new_mating_pool


""" 'Create' a single child based on two parents. Implements a bit of randomness
    to simulate nature """


def produce_offspring(parent1, parent2):
    offspring = []
    offspring_1st_half = []
    offspring_2nd_half = []

    first_gene = int(random.random() * len(parent1))
    second_gene = int(random.random() + len(parent1))
    original_gene = min(first_gene, second_gene)
    new_gene = max(first_gene, second_gene)

    for i in range(original_gene, new_gene):
        offspring_1st_half.append(parent1[i])

    offspring_2nd_half = [
        item for item in offspring_2nd_half if item not in offspring_1st_half]
    """ for chrom in parent2:
        if chrom not in offspring_1st_half:
            offspring_2nd_half.append(chrom)
 """
    offspring = offspring_1st_half+offspring_2nd_half

    return offspring


""" Breeds the population to create new offsprings.
    This algorithm doens't handle 'incest' """


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


def mutate_single(individual, mutation_prob):
    for original in range(len(individual)):
        if(random.random() < mutation_prob):
            change_original = int(random.random()*len(individual))
            city_placeholder1 = individual[original]
            city_placeholder2 = individual[change_original]
            individual[original] = city_placeholder2
            individual[change_original] = city_placeholder1
    return individual


def mutate_population(population, mutation_prob):
    new_population = []

    for i in range(0, len(population)):
        new_mutation = mutate_single(population[i], mutation_prob)
        new_population.append(new_mutation)

    return new_population


def create_next_population(current_population, elite_quantity, mutation_prob):
    fittest_members = determine_fittest_routes(current_population)
    mating_pool = select_mating_pool(
        current_population, fittest_members, elite_quantity)
    offspring = breed_population(mating_pool, elite_quantity)
    new_generation = mutate_population(offspring, mutation_prob)
    return new_generation


def genetic_algorithm(population, population_quantity, elite_quantity, mutation_prob, iterations):
    initial_population = determine_initial_population(
        population_quantity, population)
    dist_initial = determine_fittest_routes(initial_population)[0][1]
    print("Initial best distance: " + str(1/dist_initial))

    new_population = initial_population
    for _ in range(0, iterations):
        new_population = create_next_population(
            new_population, elite_quantity, mutation_prob)

    dist_final = determine_fittest_routes(new_population)[0][1]
    print("Final best distance: " + str(1/dist_final))

    best_route = determine_fittest_routes(new_population)[0][0]
    print("Best route for the Traveling Salesman: ",
          new_population[best_route])


city_list = []
for i in range(0, 10):
    city_list.append(CityNode(x=int(random.random() * 50),
                              y=int(random.random() * 50)))

genetic_algorithm(population=city_list, population_quantity=100,
                  elite_quantity=20, mutation_prob=0.01, iterations=1000)
