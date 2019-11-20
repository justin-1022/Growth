import header
import creature


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
    def crossover(genome1, genome2, points=1):

        #generating points of crossover
        crossSpots =([])
        while len(crossSpots) < points:
            newSpot = randRange(1, len(genome1)-2)
            crossSpots.add(newSpot)

        flipFlop = False#false for genome 1
        childGenome = np.array()
        for i in range(len(crossSpots)):
            #adding segments from genomes split at crossSpots
            spot = crossSpots[i]

            if i == 0:
                childGenome.append(genome1[0:spot])
                flipFlop = not flipFlop
                continue

            lastSpot = crossSpots[i-1]
            if flipFlop:
                childGenome.append(genome2[lastSpot:spot])
                if i == len(crossSpots)-1:
                    #adding last piece
                    childGenome.append(genome1[spot:])

                flipFlop = not flipFlop

            else:
                childGenome.append(genome1[lastSpot:spot])
                if i == len(crossSpots)-1:
                    #adding last piece
                    childGenome.append(genome2[spot:])

                flipFlop = not flipFlop

        return childGenome
