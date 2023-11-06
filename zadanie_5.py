import random


def create_population(size, num_cities):
    population = []
    for _ in range(size):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population


def calculate_fitness(individual, distances):
    total_distance = 0
    for i in range(len(individual) - 1):
        city_a = individual[i]
        city_b = individual[i + 1]
        total_distance += distances[city_a][city_b]
    return total_distance


def breed(parent1, parent2):
    child = [-1] * len(parent1)
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child[start:end] = parent1[start:end]

    for i in range(len(parent2)):
        if parent2[i] not in child:
            for j in range(len(child)):
                if child[j] == -1:
                    child[j] = parent2[i]
                    break
    return child


def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual


def evolve(population, distances, mutation_rate, elitism_rate):
    next_generation = []

    ranked_population = sorted(population, key=lambda x: calculate_fitness(x, distances))

    elitism_size = int(len(ranked_population) * elitism_rate)
    next_generation.extend(ranked_population[:elitism_size])

    while len(next_generation) < len(population):
        parent1 = random.choice(ranked_population[:elitism_size])
        parent2 = random.choice(ranked_population[:elitism_size])
        child = breed(parent1, parent2)
        child = mutate(child, mutation_rate)
        next_generation.append(child)

    return next_generation


def find_best_route(cities, distances, population_size=100, num_generations=100, mutation_rate=0.01, elitism_rate=0.1):
    num_cities = len(cities)

    population = create_population(population_size, num_cities)

    for _ in range(num_generations):
        population = evolve(population, distances, mutation_rate, elitism_rate)

    best_individual = min(population, key=lambda x: calculate_fitness(x, distances))
    best_route = [cities[i] for i in best_individual]

    return best_route


# Пример использования
cities = ['A', 'B', 'C', 'D', 'E']
distances = [
    [0, 2, 3, 5, 7],
    [2, 0, 4, 6, 3],
    [3, 4, 0, 2, 1],
    [5, 6, 2, 0, 4],
    [7, 3, 1, 4, 0]
]

best_route = find_best_route(cities, distances)
print(best_route)