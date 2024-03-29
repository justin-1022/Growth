import numpy as np
import random
"""vSTART
Generate the initial population
Compute fitness
REPEAT
    Selection
    Crossover
    Mutation
    Compute fitness
UNTIL population has converged
STOP"""
class Genetics:
    def __init__(self):
        self.validRanges = None

    @staticmethod
    def mutate(inputAr, mutationRate=0.05, bounds=(0, 15)):
        #bounds is tuple with max and min val for whole array
        output = np.copy(inputAr)

        arrayLen = np.shape(inputAr)[0]

        #list of tuples with index and change made
        mutationTracker = []

        for x in range(arrayLen):
            luck = random.random()

            if luck < (mutationRate/2):
                #insertions
                newGene = random.randint(bounds[0], bounds[1])

                output[x] = newGene
                mutationTracker.append((x, newGene))

            elif luck > 1 - (mutationRate/2):
                #swaps
                swapX = random.randint(0, arrayLen-1)

                output[x], output[swapX] = output[swapX], output[x]
                mutationTracker.append((x, swapX, inputAr[swapX], inputAr[x]))

        return (output, mutationTracker, len(mutationTracker))

    @staticmethod
    def selector(population):
        for creature in population:

        return newPopulation

    @staticmethod
    def crossover(population):
        return (remnants, offspring)

#basic template
class Creature:
    def __init__(self):
        self.fitness;
        self.genome;
        self.mutationRate;

        #calculated from genome
        self.hP;
        self.speed;
        self.energyNeeds;
        self.carnivore;

exGenome = np.random.random((100,)) * 15
exGenome = exGenome.astype(int)
print(Genetics.mutate(exGenome)[1])

a = np.random.random((10, 10))
b = np.random.random((10, 5))

c = np.dot(a, b)
print(c)
