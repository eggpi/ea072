import sys
import random

MAX_IT = 100
STARTING_GEN = 50

def create_random_solution(size):
    msquare = [[]] * size

    for i in range(0, size):
        msquare[i] = [random.randint(1, size * size) for x in range(0, size)]

    return msquare

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
    s = 0

    i = 0
    for el in solution:
        s += el[i]
        s += el[len(solution) - i - 1]

    return s
    
def sum_matrix(solution):
    s = 0

    for el in solution:
        for n in el:
            s += n

    return 2*s

def calc_fitness(solution, magic_num):
    s = sum_diag(solution)
    s += sum_matrix(solution)

    return abs(s - 2 * (len(solution) * magic_num) - 2 * magic_num)

def create_next_gen(size, cur_gen):
    

def store(solution, path):
    with open(path, "w") as f:
        for row in solution:
            f.write(str(row) + "\n")

def solve(size, max_it=MAX_IT):
    gen = create_starting_generation(size)

    for i in range(0, max_it):

