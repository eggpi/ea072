import sys
import random

MAX_IT = 100
STARTING_GEN = 50
MAGIC_NUM = 0

def create_random_solution(size):
    msquare = [[]] * size

    for i in range(0, size):
        msquare[i] = [random.randint(1, size * size) for x in range(0, size)]

    return [msquare, calc_fitness(msquare)] 

def create_starting_generation(size, starting_gen=STARTING_GEN):
    pop = []

    for i in range(0, starting_gen):
        pop.append(create_random_solution(size))

    return pop

def sum_cols(solution):
    s = 0

    for c in solution:
        for n in c:
            s += n

    return s

def calc_magic_constant(size):
    return (size * (size * size + 1)) / 2

def sum_diag(solution):
    d1 = 0
    d2 = 0

    i = 0
    for el in solution:
        d1 += el[i]
        d2 += el[len(solution) - i - 1]
        i += 1

    return abs(d1 - MAGIC_NUM) + abs(d2 - MAGIC_NUM)
   
def sum_rows(solution):
    s = 0

    for j in range(0, len(solution)):
        r = 0
        for i in range(0, len(solution)):
            r += solution[i][j]
        s += abs(r - MAGIC_NUM)

    return s

def sum_cols(solution):
    s = 0

    for j in range(0, len(solution)):
        r = 0
        for i in range(0, len(solution)):
            r += solution[j][i]
        s += abs(r - MAGIC_NUM)

    return s

def sum_matrix(solution):
    s = 0

    for el in solution:
        for n in el:
            s += n

    return 2*s

def calc_fitness(solution):
    s = sum_diag(solution)
    s += sum_rows(solution)
    s += sum_cols(solution)

    return s

def mutate(solution, size):
    p1 = (random.randint(0, size - 1), random.randint(0, size - 1))
    p2 = (random.randint(0, size - 1), random.randint(0, size - 1))
    sol = solution[0]

    tmp = sol[p1[0]][p1[1]]
    sol[p1[0]][p1[1]] = sol[p2[0]][p2[1]]
    sol[p2[0]][p2[1]] = tmp

    new = calc_fitness(sol)

    if new < solution[1]:
        solution[1] = new
    else:
        tmp = sol[p1[0]][p1[1]]
        sol[p1[0]][p1[1]] = sol[p2[0]][p2[1]]
        sol[p2[0]][p2[1]] = tmp

def create_next_gen(cur_gen, size, k=0.7):
    for s in cur_gen:
        mutate(s, size)
   
    return cur_gen

def store(solution, path):
    with open(path, "w") as f:
        for row in solution:
            f.write(str(row) + "\n")

def get_best(cur_gen):
    score = float("inf")
    idx = 0
    i = 0

    for s in cur_gen:
        if s[1] < score:
            score = s[1]
            idx = i
        i += 1

    return idx

def solve(size, max_it=MAX_IT, starting_gen=STARTING_GEN):
    global MAGIC_NUM
    MAGIC_NUM = calc_magic_constant(size)

    best = float("inf")
    best_idx = -1

    gen = create_starting_generation(size, starting_gen)
    best_idx = get_best(gen)
    best = gen[best_idx][1]
    print best

    for i in range(0, max_it):
        next_gen = create_next_gen(gen, size)
        gen = next_gen

        idx = get_best(gen)
        cur = gen[idx][1]
        if cur < best:
            best = cur
            print best
            best_idx = idx

        if best == 0:
            break

def get_idx(args, param):
    i = 0
    for arg in args:
        if arg == param:
            return i
        i += 1
    return -1

max_it = MAX_IT
idx = get_idx(sys.argv, "-it")
if idx != -1:
    max_it = int(sys.argv[idx+1])

starting_gen = STARTING_GEN
idx = get_idx(sys.argv, "-st")
if idx != -1:
    starting_gen = int(sys.argv[idx+1])

solve(int(sys.argv[1]), max_it, starting_gen)
