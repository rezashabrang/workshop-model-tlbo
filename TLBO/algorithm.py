import random
from MODEL.model import TEC
from initialization import generate_initial_randoms


# Student class
class Student:
    def __init__(self,):
        self.


# --------------------- START OF TLBO ---------------------
rnd = random.Random(0)

# create n random students
classroom = [Student(fitness, dim, minx, maxx, i) for i in range(n)]

# compute the value of best_position and best_fitness in the classroom
Xbest = [0.0 for i in range(dim)]
Fbest = sys.float_info.max

for i in range(n):  # check each Student
    if classroom[i].fitness < Fbest:
        Fbest = classroom[i].fitness
        Xbest = copy.copy(classroom[i].position)

# main loop of tlbo
Iter = 0
while Iter < max_iter:

    # after every 10 iterations
    # print iteration number and best fitness value so far
    if Iter % 10 == 0 and Iter > 1:
        print("Iter = " + str(Iter) + " best fitness = %.3f" % Fbest)

    # for each student of classroom
    for i in range(n):

        ### Teaching phase of ith student

        # compute the mean of all the students in the class
        Xmean = [0.0 for i in range(dim)]
        for k in range(n):
            for j in range(dim):
                Xmean[j] += classroom[k].position[j]

        for j in range(dim):
            Xmean[j] /= n;

        # initialize new solution
        Xnew = [0.0 for i in range(dim)]

        # teaching factor (TF)
        # either 1 or 2 ( randomly chosen)
        TF = random.randint(1, 3)

        # best student of the class is teacher
        Xteacher = Xbest

        # compute new solution
        for j in range(dim):
            Xnew[j] = classroom[i].position[j] + rnd.random() * (Xteacher[j] - TF * Xmean[j])

        # if Xnew < minx OR Xnew > maxx
        # then clip it
        for j in range(dim):
            Xnew[j] = max(Xnew[j], minx)
            Xnew[j] = min(Xnew[j], maxx)

        # compute fitness of new solution
        fnew = fitness(Xnew)

        # if new solution is better than old
        # replace old with new solution
        if (fnew < classroom[i].fitness):
            classroom[i].position = Xnew
            classroom[i].fitness = fnew

        # update best student
        if (fnew < Fbest):
            Fbest = fnew
            Xbest = Xnew

        ### learning phase of ith student

        # randomly choose a solution from classroom
        # chosen solution should not be ith student
        p = random.randint(0, n - 1)
        while (p == i):
            p = random.randint(0, n - 1)

        # partner solution
        Xpartner = classroom[p]

        Xnew = [0.0 for i in range(dim)]
        if (classroom[i].fitness < Xpartner.fitness):
            for j in range(dim):
                Xnew[j] = classroom[i].position[j] + rnd.random() * (classroom[i].position[j] - Xpartner.position[j])
        else:
            for j in range(dim):
                Xnew[j] = classroom[i].position[j] - rnd.random() * (classroom[i].position[j] - Xpartner.position[j])

        # if Xnew < minx OR Xnew > maxx
        # then clip it
        for j in range(dim):
            Xnew[j] = max(Xnew[j], minx)
            Xnew[j] = min(Xnew[j], maxx)

        # compute fitness of new solution
        fnew = fitness(Xnew)

        # if new solution is better than old
        # replace old with new solution
        if (fnew < classroom[i].fitness):
            classroom[i].position = Xnew
            classroom[i].fitness = fnew

        # update best student
        if (fnew < Fbest):
            Fbest = fnew
            Xbest = Xnew

    Iter += 1
# end-while
