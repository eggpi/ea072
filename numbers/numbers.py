import random
import sys
import collections

LOCAL_SEARCH = False
MAX_ITERATIONS = 1000
STARTING_INDIVIDUALS = 100

# An individual in our solution space.
# The genome is a binary list where 0 and 1 are the different sets
Individual = collections.namedtuple("Individual", ("genome", "fitness"))

def read_numbers(path):
    nums = []

    with open(path) as f:
        for n in f:
            nums.append(int(n.strip()))

    return nums

def split_sets(genome, numbers):
    sets = [[], []]
    for s, n in zip(genome, numbers):
        sets[s].append(n)

    return sets[0], sets[1]

def fitness(genome, numbers):
    s1, s2 = split_sets(genome, numbers)
    return abs(sum(s1) - sum(s2))

def save_numbers(ind, path, numbers):
    s1, s2 = split_sets(ind.genome, numbers)
    with open(path, "w") as f:
        print >> f, "Fitness: %s" % ind.fitness
        print >> f, s1
        print >> f, s2

def create_random_individual(numbers):
    genome = []
    for _ in numbers:
        genome.append(random.choice((0, 1)))

    return Individual(genome, fitness(genome, numbers))

def mutate(generation, numbers):
    # flip a random bit with probability of 0.03 for each individual
    N = len(numbers)
    for i, ind in enumerate(generation):
        if random.random() < 0.05:
            bitidx = random.randint(0, N-1)
            genome = ind.genome
            genome[bitidx] = (genome[bitidx] + 1) % 2

            generation[i] = Individual(genome, fitness(genome, numbers))

def cross_over(generation, numbers):
    # use a roulette wheel to pick N/2 pairs of individuals for
    # crossing over
    EPS = 1e-6
    inv_fitness = [1.0 / (EPS + ind.fitness) for ind in generation]
    total_fitness = sum(inv_fitness)
    fitness_ratios = [invf / total_fitness for invf in inv_fitness]

    cumsum = [0]
    for fr in fitness_ratios:
        fr += cumsum[-1]
        cumsum.append(fr)
    cumsum.pop(0)

    to_cross = []
    for _ in generation:
        p = random.random()
        for i, ps in enumerate(cumsum):
            if ps > p:
                to_cross.append(generation[i])
                break
        else:
            assert False

    # cross over using a random point
    next_generation = []
    for ind1, ind2 in zip(to_cross[::2], to_cross[1::2]):
        crossing_point = random.randint(0, len(generation))

        genome = ind1.genome[:crossing_point] + ind2.genome[crossing_point:]
        next_generation.append(Individual(genome, fitness(genome, numbers)))

        genome = ind2.genome[:crossing_point] + ind1.genome[crossing_point:]
        next_generation.append(Individual(genome, fitness(genome, numbers)))

    assert len(next_generation) == len(generation)
    return next_generation

def create_next_generation(generation, numbers):
    next_generation = cross_over(generation, numbers)
    mutate(next_generation, numbers)

    if LOCAL_SEARCH:
        for indidx, ind in enumerate(next_generation):
            s1, s2 = split_sets(ind.genome, numbers)
            sum1, sum2 = sum(s1), sum(s2)

            diff = sum1 - sum2
            if diff > 0:
                bigger_set = s1
            else:
                bigger_set = s2

            # find the biggest number we can move from the
            # set with largest sum to the set with lowest sum
            # to make the difference smaller
            diff = abs(diff)
            bigger_set.sort()
            for nidx in range(len(bigger_set) - 1):
                if bigger_set[nidx + 1] > diff / 2:
                    break

            n = bigger_set[nidx]
            if n > diff / 2:
                continue

            gidx = numbers.index(n)

            genome = ind.genome
            genome[gidx] = (genome[gidx] + 1) % 2

            new_fitness = fitness(genome, numbers)
            assert new_fitness <= ind.fitness
            next_generation[indidx] = Individual(genome, new_fitness)

    return next_generation

def get_best_individual(generation):
    best = Individual([], float("inf"))
    for ind in generation:
        if ind.fitness < best.fitness:
            best = ind

    assert best.genome
    return best

def save_debug_info(debug, path):
    with open(path, "w") as f:
        for d in debug:
            f.write("Iteration: " + str(d[1]) + " Score: " + str(d[0]) + "\n")

def solve(numbers, starting_inds = STARTING_INDIVIDUALS, max_it=MAX_ITERATIONS):
    best = -1
    generation = []
    random.seed()

    debug = []

    # Create starting random generation
    for i in range(0, starting_inds):
        generation.append(create_random_individual(numbers))

    # Iterate while keeping track of the best individual
    best_individual = get_best_individual(generation)
    for i in range(0, max_it):
        next_generation = create_next_generation(generation, numbers)
        next_best = get_best_individual(next_generation)
        if next_best.fitness < best_individual.fitness:
            best_individual = next_best
        generation = next_generation
        debug.append([best_individual.fitness, i + 1])
        print >> sys.stderr, "\rGeneration %s" % (i + 1),

    print >> sys.stderr
    return best_individual, debug

numbers = read_numbers(sys.argv[1])
best, debug = solve(numbers)
save_debug_info(debug, sys.argv[2])
save_numbers(best, sys.argv[3], numbers)
