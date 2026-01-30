import math
import random

def paths(total):
    random_paths = []
    for index in range(1000):
        random_path = list(range(1, total))
        random.shuffle(random_path)
        random_path = [0] + random_path
        random_paths.append(random_path)

    return random_paths

cities = [
    (10, 20), (80, 90), (30, 70), (90, 30), (50, 50),
    (20, 80), (70, 20), (40, 60), (60, 10), (15, 45),
    (25, 85), (75, 35), (45, 55), (85, 15), (35, 75)
]

def distance(cities, path):
    total = 0
    for i in range(len(path) - 1):
        city1 = cities[path[i]]
        city2 = cities[path[i +1]]
        x1 = city1[0]
        x2=city2[0]
        y1=  city1[1]
        y2=  city2[1]
        dx = x2 - x1
        dy =  y2 - y1
        dist = math.sqrt(dx*dx + dy*dy)
        total = total + dist
    return total

#Survivors
def selection(cities, old_generation):
    selected = []
    random.shuffle(old_generation)
    mid = len(old_generation) // 2
    for i in range(mid):
        if distance(cities, old_generation[i]) <distance(cities, old_generation[i + mid]):
            selected.append(old_generation[i])
        else:
            selected.append(old_generation[i + mid])
    return selected

def offspring(parent1, parent2):
    start = random.randint(1, len(parent1) - 1)
    finish = random.randint(start, len(parent1))

    from_parent1 = []
    from_parent2 = []
    
    for i in range(start, finish):
        from_parent1.append(parent1[i])
    for part in parent2:
        if part not in from_parent1:
            from_parent2.append(part)
    final = []
    parent2_index = 0
    for i in range(len(parent1)):
        if i >= start and i < finish:
            final.append(from_parent1[i - start])
        else:
            final.append(from_parent2[parent2_index])
            parent2_index = parent2_index + 1
    return final

# Crossover
def crossover(selected):
    offsprings = []
    mid = len(selected) // 2
    
    for i in range(mid):
        parent1 = selected[i]
        parent2 = selected[i + mid]
        for idx in range(2):
            offsprings.append(offspring(parent1, parent2))
            offsprings.append(offspring(parent2, parent1))
    return offsprings

#Mutation with 25% probability.
def mutate(generation):
    mutated = []
    for path in generation:
        if random.randint(0, 100) < 25:
            index1 = random.randint(1, len(path) - 1)
            index2 = random.randint(1, len(path) - 1)
            path[index1], path[index2] = path[index2], path[index1]
        mutated.append(path)
    return mutated

def new_generation(cities, old_generation):
    selected = selection(cities, old_generation)
    offsprings = crossover(selected)
    new_population = mutate(offsprings)
    return new_population

if __name__ == "__main__":
    population = paths(15)
    for gen in range(101):
        best = distance(cities, population[0])
        
        for path in population:
            current = distance(cities, path)
            if current < best:
                best = current
        print(f"Generation {gen}: Best distance = {round(best, 3)}")
        population = new_generation(cities, population)
