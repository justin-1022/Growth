import header
from genetics import Genetics

class Creature:
    def __init__(self, genome=None):
        if genome is None:
            self.genome = np.random((256,))

        else:
            self.genome = genome

        #ancestral data
        self.p2Genome = None
        self.p1Genome = None
        self.generationNumber = 0


        #calculated from genome
        self.hpMax;
        self.speed;
        self.energyReq;#cube size
        self.diet;#low vals = eats meat,high =vegan, middle = omni
        self.lifespan;

        #status data
        self.age = 0
        self.fatigue = 0
        self.awareness = 100
        self.stress = 0
        self.hp;
        self.energy;#depleted by 1/2mv^2

        #info for drawing


    def mate(self, other):
        #mating between two Creatures
        childGenome = crossover(self.genome, other.genome)
        childGenome = mutate(childGenome)[0]
        child = Creature(childGenome)
        return child

    def getPublicInfo(self, other):
        pass

"""
Genome indexing:
0-49 reserved for attributes
rest NN weights
"""
