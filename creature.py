from header import *
from genetics import Genetics
import numpy as np

class Creature:
    def __init__(self, x, y, genome=None):
        if genome is None:
            self.genome = np.random.random((256,))

        else:
            self.genome = genome

        #ancestral data
        self.p2Genome = None
        self.p1Genome = None
        self.generationNumber = 0
        self.id = random.randint(0, 10000000000)


        #calculated from genome
        self.hpMax = None
        self.speed = self.genome[GENE["speed"]]
        self.energyReq = (3*self.genome[GENE["size"]])**3
        self.diet = None#low vals = eats meat,high =vegan, middle = omni
        self.lifespan = None
        self.moveCost = 3*self.genome[GENE["size"]]/2 * self.speed**2 *0.01

        #status data
        self.age = 0
        self.fatigue = 0
        self.awareness = 100
        self.stress = 0
        self.hp = None
        self.energy = self.energyReq#depleted by 1/2mv^2

        #info for drawing
        self.size = TILESIZE * self.genome[GENE["size"]]
        self.color = Creature.getColor(self.genome)

        #locational data
        self.x = x
        self.y = y
        self.angle = 0

        self.foodSeen = []
        self.creaturesSeen = []

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Creature):
            return self.id == other.id

        else:
            return False


    def mate(self, other):
        #mating between two Creatures
        childGenome = crossover(self.genome, other.genome)
        childGenome = mutate(childGenome)[0]
        child = Creature(childGenome)
        return child

    def getPublicInfo(self, other):
        pass

    def draw(self, canvas, color=None):
        if color is None: color = self.color

        canvas.create_oval(self.x - self.size/2, self.y - self.size/2,
                self.x + self.size/2, self.y + self.size/2,
                fill=color, width=0)

    @staticmethod
    def getColor(genome):
        colorString = ""
        rgb = [genome[GENE["red"]], genome[GENE["green"]], genome[GENE["blue"]]]
        for i in range(len(rgb)):
            rgb[i] = min(int(abs(rgb[i])*255), 255)
        colorString = "#%02x%02x%02x" % tuple(rgb)

        return colorString

    def decideDemo(self):
        #[x, y, foodx, foody, foodx, foody, foodNut]
        pass

    def look(self, stuff, code):
        if code == 0:
            for item in stuff:
                dApprox = (food.x - self.x)**2 + (food.x - self.x)**2))
                if len(self.foodSeen) < 2:
                    self.foodSeen.append(food)
                    self.foodDist.append(dApprox)

                else:
                    if (dApprox < max(self.foodDist):
                        index = self.foodDist.index(max(self.foodDist))

                        self.foodSeen[index] = food
                        self.foodDist[index] = dApprox

        elif code == 1:
            for other in stuff:
                if other == self: continue
                dApprox = (other.x - self.x)**2 + (other.x - self.x)**2))
                if len(self.cretSeen) < 2:
                    self.cretSeen.append(other)
                    cret.cretDist.append(dApprox)

                else:
                    if (dApprox < max(self.cretDist):
                        index = self.cretDist.index(max(self.cretDist))

                        self.cretSeen[index] = cret2
                        self.cret2Dist[index] = dApprox



class spawnNode:
    def __init__(self, x, y, count, genome1=None, genome2=None):
        #allows for spawning either random or controlled populations
        #1 genome = clones, 2=children of those two
        self.x = x
        self.y = y
        self.g1 = genome1
        self.g2 = genome2

        self.count = count

        self.creatureSet = set([])

        self.spawnRadius = 3

    def spawnCreatures(self):
        #creating actual creatures to be added to game
        if self.g2 is not None and self.g1 is not None:
            for i in range(self.count):
                #figuring out wherre to put it
                xMult = 1 if random.random() < 0.5 else -1
                xAug = self.spawnRadius*random.random()*TILESIZE * xMult
                x = self.x + xAug

                yMult = 1 if random.random() < 0.5 else -1
                yAug = self.spawnRadius*random.random()*TILESIZE * yMult
                y = self.y + yAug

                genome = crossover(g1, g2)
                cret = Creature(x, y, genome)

                cret.p1Genome, cret.p2Genome = g1, g2

                self.creatureSet.add(Creature(genome))

        elif self.g1 is not None:
            for i in range(self.count):
                #figuring out wherre to put it
                xMult = 1 if random.random() < 0.5 else -1
                xAug = self.spawnRadius*random.random()*TILESIZE * xMult
                x = self.x + xAug

                yMult = 1 if random.random() < 0.5 else -1
                yAug = self.spawnRadius*random.random()*TILESIZE * yMult
                y = self.y + yAug

                self.creatureSet.add(Creature(x, y, self.g1))

        else:
            for i in range(self.count):
                #figuring out wherre to put it
                xMult = 1 if random.random() < 0.5 else -1
                xAug = self.spawnRadius*random.random()*TILESIZE * xMult
                x = self.x + xAug

                yMult = 1 if random.random() < 0.5 else -1
                yAug = self.spawnRadius*random.random()*TILESIZE * yMult
                y = self.y + yAug

                self.creatureSet.add(Creature(x, y))

        print("Creatures spawned:", len(self.creatureSet))


    def draw(self, canvas, color=None):
        if color is None: color = self.color

        canvas.create_oval(self.x - self.size/2, self.y - self.size/2,
                self.x + self.size/2, self.y + self.size/2,
                fill=color, width=0)

"""
Genome indexing:
0-49 reserved for attributes
rest NN weights
"""
