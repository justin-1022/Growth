import header


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
    def hardSelector(population, limit=0.5):
        minimum = len(population) * 0.5
        tempSum = 0
        for creature in population:
            tempSum += creature.fitness

        avgFitness = tempSum / len(population)

        popCount = 0
        for i in range(len(population)):
            creature = population[i-popCount]
            if creature.fitness < avgFitness:
                population.pop(i-popCount)

            if len(population) <= minimum:
                break

        return newPopulation

    @staticmethod
    def luckSelector(population, limit=0.5):
        minimum = len(population) * 0.5
        tempSum = 0
        for creature in population:
            tempSum += creature.fitness

        avgFitness = tempSum / len(population)

        popCount = 0
        for i in range(len(population)):
            creature = population[i-popCount]

            luck = creature.fitness/(2*avgFitness)
            fate = random.random()

            if luck < fate:
                population.pop[i-popCount]

            if len(population) <= minimum:
                break

            
    @staticmethod
    def crossover(population):
        return (remnants, offspring)
