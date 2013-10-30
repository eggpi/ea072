from optparse import OptionParser
import re
import sys
import random

MAX_IT = 200
STARTING_GENS = 30

def read_tsp(path):
    cities = []
    with open(path) as f:
        for line in f:
            data = re.search("([0-9]*) *([0-9]*.[0-9]*) *([0-9]*.[0-9]*)", line.strip("\r\n"))
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
        print "Best: " + str(solution[1])
        f.write("Score: " + str(solution[1]) + "\n")
        f.write("TSP Solution: " + str(solution[0]))

def mutate(cities, sol):
    solution = list(sol)
    pos = random.randint(0, len(solution[0]) - 1)
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

    return solution

def swap_nearest_neighbors(cities, solution):
    for i in range(0, len(solution) - 2):
        city = solution[i]
        city2 = solution[i+1]
        city3 = solution[i+2]
        dab = calc_distance(cities[city][0], cities[city][1], cities[city2][0], cities[city2][1])
        dac = calc_distance(cities[city][0], cities[city][1], cities[city3][0], cities[city3][1])
        dbc = calc_distance(cities[city2][0], cities[city2][1], cities[city3][0], cities[city3][1])

        if dac < dab + dbc:
            tmp = solution[i+1]
            solution[i+1] = solution[i+2]
            solution[i+2] = tmp

def cross_over(cities, s1, s2):
    cut1 = random.randint(0, len(s1[0]) - 1)
    cut2 = random.randint(cut1, len(s1[0]) - 1)

    child = s1[0][cut1:cut2]
    for x in s2[0]:
        if x not in child:
            child.append(x)

#    swap_nearest_neighbors(cities, child)

    return [child, calc_total_distance(cities, child)]

def create_next_generation(cities, cur_gen):
    population = [[]]*len(cur_gen)
    i = 0

    for sol in cur_gen:
        population[i] = mutate(cities, sol)
        swap_nearest_neighbors(cities, population[i])

        tmp = cross_over(cities, population[i], 
                cur_gen[random.randint(0, len(cur_gen)-1)]) 
        if tmp[1] < population[i][1]:
            population[i] = tmp
        #population[i] = mutate(cities, sol)

        #swap_nearest_neighbors(cities, population[i])
        #population[i] = mutate(cities, sol)
        i += 1

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

def solve(cities, debug_dir, starting_gens=STARTING_GENS, max_it=MAX_IT):
    random.seed()
    population = []
    debug = [] #debug = [it_num, solution]

    # create initial population
    for i in range(0, starting_gens - 1):
        population.append(create_random_solution(cities))

    debug.append([0, list(get_best_sol(population))])
    best = debug[0][1][1]

    for i in range(0, max_it):
        next_pop = create_next_generation(cities, population)
        tmp = get_best_sol(next_pop)

        if tmp[1] < best:
            print best, tmp[1]
            debug.append([i+1, list(tmp)])
            best = tmp[1]

        population = next_pop

    save_debug(debug_dir, debug)

    return get_best_sol(population)

parser = OptionParser()
parser.add_option("-i", "--input", action="store", 
        type="string", dest="input", help="input tsp file")
parser.add_option("-o", "--output", dest="output", 
        action="store", type="string", help="output results to file")
parser.add_option("-d", "--debug", dest="debug", 
        action="store", type="string", help="outputs debug info to file")
parser.add_option("-m", "--max_it", dest="max_it", default=MAX_IT,
        action="store", type="int", help="max number of iterations")
parser.add_option("-s", "--sg", dest="starting_gen", default=STARTING_GENS,
        action="store", type="int", help="starting generations")

(options, args) = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    quit()

save_solution(options.output, solve(read_tsp(options.input), options.debug, options.max_it, options.starting_gen))
