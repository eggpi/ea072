import random
import sys

STARTING_GENERATIONS = 100
MAX_ITERATIONS = 120
LOCAL_SEARCH = True
LOCAL_SEARCH_MIN = 1
LOCAL_SEARCH_MAX = 5

def read_numbers(path):
    nums = []

    with open(path) as f:
        for n in f:
            nums.append(int(n.strip()))

    return nums

def calc_fitness(set1, split):
    s1 = 0
    s2 = 0

    for i in range(0, split):
        s1 += set1[i]

    for i in range(split, len(set1)):
        s2 += set1[i]

    return int(abs(s1 - s2))

def save_numbers(set1, path):

    with open(path, "w") as f:
        f.write("Score: " + str(set1[2]) + "\n")
        print str(set1[2]) + "\n"
        f.write("Set 1: " + str(set1[0][:set1[1]]) + "\n")
        f.write("Set 2: " + str(set1[0][set1[1]:]))

def create_random_generation(numbers):
    copy = list(numbers)
    s1 = []

    split = random.randint(0, len(copy) - 1)
    while len(copy) > 0:
        pos = random.randint(0, len(copy) - 1)
        s1.append(copy[pos])
        del copy[pos]

    return [s1, split, calc_fitness(s1, split)]

def mutate(current_gen):
    pos = random.randint(0, len(current_gen[0]) - 1)

    new = calc_fitness(current_gen[0], pos)
    if current_gen[2] > new:
        current_gen[1] = pos
        current_gen[2] = new

    if LOCAL_SEARCH:
        neigh = random.randint(LOCAL_SEARCH_MIN, LOCAL_SEARCH_MAX)
        start = current_gen[1] - neigh
        end = current_gen[1] + neigh

        if start < 0:
            start = 0
        if end > len(current_gen[0]):
            end = len(current_gen[0])

        for i in range(start, end):
            new = calc_fitness(current_gen[0], i)
            if current_gen[2] > new:
                current_gen[1] = i
                current_gen[2] = new

def cross_over(gen, current_gen):
    gen2 = current_gen[random.randint(0, len(current_gen[0]) - 1)]
  
    new = calc_fitness(gen[0], (gen[1] + gen2[1]) / 2)
    if new < gen[2]:
        gen[1] = (gen[1] + gen2[1]) / 2
        gen[2] = new

    if LOCAL_SEARCH:
        neigh = random.randint(LOCAL_SEARCH_MIN, LOCAL_SEARCH_MAX)
        start = gen[1] - neigh
        end = gen[1] + neigh

        if start < 0:
            start = 0
        if end > len(gen[0]):
            end = len(gen[0])

        for i in range(start, end):
            new = calc_fitness(gen[0], i)
            if gen[2] > new:
                gen[1] = i
                gen[2] = new

def generate_next_gen(gen, current_gen):
    prob = random.uniform(0, 1)

    #if prob <= 0.12:
    #mutate(gen)
    #mutate(gen)
    cross_over(gen, current_gen)
    #cross_over(gen, current_gen)
    mutate(gen)
    #elif prob <= 0.24:
    #    cross_over(gen, current_gen)
    #elif prob <= 0.8:
    #    mutate(gen)
    #    cross_over(gen, current_gen)
    #else:
    #    cross_over(gen, current_gen)
    #    mutate(gen)

    return gen

def get_best_score(generations):
    best = float("inf")
    index = 0
    i = 0

    for g in generations:
        if g[2] < best:
            best = g[2]
            index = i
        i += 1

    return index

def save_debug_info(debug, path):
    with open(path, "w") as f:
        for d in debug:
            f.write("Iteration: " + str(d[1]) + " Score: " + str(d[0]) + "\n")

def solve(numbers, starting_gens=STARTING_GENERATIONS, max_it=MAX_ITERATIONS):
    best = -1
    best_gen = []
    generation = []
    random.seed()

    debug = []

    # Create starting random generation
    for i in range(0, starting_gens):
        generation.append(create_random_generation(numbers))

    # Store the best result from the first generation
    best_gen = generation[get_best_score(generation)]
    debug.append([best_gen[2], 0])

    for i in range(0, max_it):
        next_generation = []
        for gen in generation:
            next_generation.append(generate_next_gen(gen, generation))
       
        new_best = get_best_score(next_generation)
        if next_generation[new_best][2] < best_gen[2]:
            best_gen = next_generation[new_best]
            debug.append([best_gen[2], i + 1])

    return best_gen, debug

numbers = read_numbers(sys.argv[1])
best, debug = solve(numbers)
save_debug_info(debug, sys.argv[2])
save_numbers(best, sys.argv[3])
