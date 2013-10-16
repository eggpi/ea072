import re
import sys
import random

MAX_IT = 200
STARTING_GENS = 30

def read_tsp(path):
    cities = []
    with open(path) as f:
        for line in f:
            data = re.search("([0-9]*) *([0-9]*.[0-9]*) *([0-9]*.[0-9]*)",line.strip("\r\n"))
            cities.append([int(data.group(1)), float(data.group(2)), float(data.group(3))])

    return cities

def calc_distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def calc_total_distance(cities, path):
    dist = 0

    for x in range(-1, len(path) - 1):
        cur = cities[path[x]]
        cur2 = cities[path[x+1]]
        dist += calc_distance(cur[1], cur[2], cur2[1], cur2[2])

    return dist

def create_random_solution(cities):
    solution = []
    hold = [i for i in range(0, len(cities))]

    for i in range(0, len(cities)):
        rnd = random.randint(0, len(hold) - 1)
        solution.append(hold[rnd])
        del hold[rnd]

    return [solution, calc_total_distance(cities, solution)]

def save_solution(path, solution):
    with open(path, "w") as f:
        print solution[1]
        f.write("Score: " + str(solution[1]) + "\n")
        f.write("Hamiltonian Cycle: " + str(solution[0]))

def mutate2(cities, solution):
    num = 0.3 * len(cities)
    if num == 0:
        num = 1

    while num > 0:
        pos = random.randint(0, len(solution[0]) - 1)
        pos2 = pos

        # Avoid swaping with himself
        while pos == pos2:
            pos2 = random.randint(0, len(solution[0]) - 1)
    
        # swap random city
        city = solution[0][pos]
        solution[0][pos] = solution[0][pos2]
        solution[0][pos2] = city
        
        num -= 1

        new_dist = calc_total_distance(cities, solution[0])
        if new_dist < solution[1]:
            # update distance
            solution[1] = new_dist
        else:
            # unswap if solution was not improved
            city = solution[0][pos]
            solution[0][pos] = solution[0][pos2]
            solution[0][pos2] = city


def mutate(cities, solution):
    pos = random.randint(0, len(solution[0]) - 1)
    pos2 = pos

    # Avoid swaping with himself
    while pos == pos2:
        pos2 = random.randint(0, len(solution[0]) - 1)
    
    # swap random city
    city = solution[0][pos]
    solution[0][pos] = solution[0][pos2]
    solution[0][pos2] = city

    new_dist = calc_total_distance(cities, solution[0])
    if new_dist < solution[1]:
        # update distance
        solution[1] = new_dist
    else:
        # unswap if solution was not improved
        city = solution[0][pos]
        solution[0][pos] = solution[0][pos2]
        solution[0][pos2] = city

def cross_over(cities, s1, s2):
    cut = random.randint(0, len(s1[0]))

    child = s1[0][:cut]
    for x in s2[0]:
        if x not in child:
            child.append(x)

    return [child, calc_total_distance(cities, child)]

def create_next_generation(cities, cur_gen):
    population = list(cur_gen)
    for sol in population:
        mutate2(cities, sol)
        p1 = random.randint(0, len(population) - 1)
        sol = cross_over(cities, sol, population[p1])

    return population

def get_best_sol(population):
    idx = 0
    dist = float("inf")
    i = 0

    for sol in population:
        if sol[1] < dist:
            dist = sol[1]
            idx = i
        i += 1

    return population[idx]

def save_debug(path, debug):
    with open(path, "w") as f:
        for sol in debug:
            f.write("Iteration: " + str(sol[0]) + "\n")
            f.write("Score: " + str(sol[1][1]) + "\n")
            f.write("Solution: " + str(sol[1][0]) + "\n")

def solve(cities, starting_gens=STARTING_GENS, max_it=MAX_IT):
    random.seed()
    population = []
    debug = []

    # create initial population
    for i in range(0, starting_gens - 1):
        population.append(create_random_solution(cities))

    debug.append([0, list(get_best_sol(population))])
    best = debug[0][1][1]

    for i in range(0, max_it):
        next_pop = create_next_generation(cities, population)
        tmp = get_best_sol(next_pop)

        if tmp[1] < best:
            debug.append([i+1, list(tmp)])
            best = tmp[1]

        population = next_pop

    save_debug(sys.argv[2], debug)

    return get_best_sol(population)
    
save_solution(sys.argv[3], solve(read_tsp(sys.argv[1])))
