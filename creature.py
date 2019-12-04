from header import *
from genetics import Genetics
import numpy as np
from environment import *
from decisions import *

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
        self.speed = self.genome[GENE["agi"]]
        self.energyReq = (3*self.genome[GENE["size"]])**3
        self.diet = None#low vals = eats meat,high =vegan, middle = omni
        self.lifespan = None
        self.moveCost = 3*self.genome[GENE["size"]]/2 * self.speed**2 * 0.01

        #status data
        self.age = 0
        self.fatigue = 0
        self.awareness = 100
        self.stress = 0
        self.hp = None
        self.energy = self.energyReq#depleted by 1/2mv^2

        #info for drawing
        self.size = 10 + (TILESIZE-10) * self.genome[GENE["size"]]
        self.color = Creature.getColor(self.genome)

        #locational data/movement
        self.x = x
        self.y = y
        self.velX = 0
        self.velY = 0
        self.angle = 0

        self.foodSeen = []
        self.foodDist = []
        self.cretSeen = []
        self.cretDist = []
        self.infoVector = []

        #decision stuff
        self.w1 = self.genome[50:92]
        self.w1 = np.reshape(self.w1, (3, 14))

        self.w2 = self.genome[92:104]
        self.w2 = np.reshape(self.w2, (4, 3))

        self.w3 = self.genome[104:124]
        self.w3 = np.reshape(self.w3, (5, 4))

        self.b1 = self.genome[124:127]
        self.b1 = np.vstack(self.b1)

        self.b2 = self.genome[127:131]
        self.b2 = np.vstack(self.b2)

        self.b3 = self.genome[131:136]
        self.b3 = np.vstack(self.b3)

        #for idling
        self.isIdle = False
        self.idleTime = 0


        #asset management
        self.markForDelete = False
        self.safe = False
        self.eaten = set([])

        #for evolving
        self.fitness = 0

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Creature):
            return self.id == other.id

        else:
            return False


    def mate(self, other):
        #mating between two Creatures
        childGenome = Genetics.crossover(self.genome, other.genome)
        childGenome = Genetics.mutate(childGenome)[0]
        x = random.randint(0,WIDTH)
        y = random.randint(0, HEIGHT)
        child = Creature(x, y, childGenome)
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

    def decide(self):
        #[x, y, foodx, foody, foodNut, Cretx, crety]
        if not self.isIdle:
            self.infoVector = [self.x, self.y]

            if len(self.foodSeen) > 0:
                self.infoVector.extend([self.foodSeen[0].x, self.foodSeen[0].y])
                self.infoVector.append(self.foodSeen[0].energy)

            else:
                self.infoVector.extend([-1, -1, -1])

            if len(self.foodSeen) > 1:
                self.infoVector.extend([self.foodSeen[1].x, self.foodSeen[1].y])
                self.infoVector.append(self.foodSeen[1].energy)

            else:
                self.infoVector.extend([-1, -1, -1])


            if len(self.cretSeen) > 0:
                self.infoVector.extend([self.cretSeen[0].x, self.cretSeen[0].y,
                self.cretSeen[0].speed])

            else:
                self.infoVector.extend([-1, -1, -1])

            if len(self.cretSeen) > 1:
                self.infoVector.extend([self.cretSeen[1].x, self.cretSeen[1].y,
                self.cretSeen[0].speed])

            else:
                self.infoVector.extend([-1, -1, -1])



            self.infoVector = np.vstack(np.array(self.infoVector))

            self.decisionVector = feedForward(self.infoVector, self.w1, self.w2,
            self.w3, self.b1, self.b2, self.b3)

            if self.decisionVector[4] > self.decisionVector[0]:
                for food in self.foodSeen:
                    self.eat(food)

            else:
                self.move(self.decisionVector[1], self.decisionVector[2],
                                self.decisionVector[3])

        #[move?, x, y, angle, eat?]



    def move(self, fX, fY, angle):
#        print(self.id, "moving", self.x, self.y)
        self.velX = fX * self.speed * 1000
        self.velY = fY * self.speed * 1000
        self.angle = angle * math.pi

    def eat(self, food):

        if (self.x-food.x)**2 + (self.y-food.y)**2 <= self.size**2:
            if not isinstance(food, Corpse):
                self.energy += food.energy
                food.markForDelete = True
                self.fitness += 1
                self.safe = True
#                print(self.id, "eating")
                self.idle(food.energy)

                self.eaten.add(food)
                print([food.id for food in self.eaten])



    def update(self, dt):
#        print(self.id, "updating")
        self.energy -= self.energyReq * dt
        self.age += dt

        self.x += float(self.velX * math.cos(self.angle*2*math.pi) * dt)
        self.y += float(self.velY * math.sin(self.angle*2*math.pi) * dt)

        if self.velX > 0:
            self.velX *= 0.5 + 0.02*self.size

        if self.velY > 0:
            self.velY *= 0.5 + 0.02*self.size

        if self.x - self.size < 0:
            self.x = self.size/2

        elif self.x + self.size > WIDTH:
            self.x = WIDTH - self.size/2

        if self.y - self.size < 0:
            self.y = self.size/2

        elif self.y + self.size > HEIGHT:
            self.y = HEIGHT - self.size/2

#        self.fitness = self.energy / self.energyReq

        if self.energy < 0 and not self.safe: self.markForDelete = True

        self.idle()

    def idle(self, time=0):
        if time > 0:
#            print(self.id, "going idle")
            self.isIdle = True
            self.idleTime = time

        elif self.idleTime > 0:
            self.idleTime -= 1

        elif self.idleTime == 0:
#            print(self.id, "waking up")
            self.isIdle = False

    def makeCorpse(self):
        #makes a corpse food object upon death
        pass

    def look(self, stuff, code):
#        print(self.id, "looking")
        if code == 0:
            for food in stuff:
                dApprox = (food.x - self.x)**2 + (food.x - self.x)**2
                if len(self.foodSeen) < 2:
                    self.foodSeen.append(food)
                    self.foodDist.append(dApprox)

                else:
                    if dApprox < max(self.foodDist):
                        index = self.foodDist.index(max(self.foodDist))

                        self.foodSeen[index] = food
                        self.foodDist[index] = dApprox

        elif code == 1:
            for other in stuff:
                if other == self: continue
                dApprox = (other.x - self.x)**2 + (other.x - self.x)**2
                if len(self.cretSeen) < 2:
                    self.cretSeen.append(other)
                    self.cretDist.append(dApprox)

                else:
                    if dApprox < max(self.cretDist):
                        index = self.cretDist.index(max(self.cretDist))

                        self.cretSeen[index] = other
                        self.cretDist[index] = dApprox


#        print(self.id, len(self.cretSeen), len(self.foodSeen), "saw")



class SpawnNode:
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
        self.color = "black"
        self.size = TILESIZE

    def spawnCreatures(self):
        #creating actual creatures to be added to game
        if self.g2 is not None and self.g1 is not None:
            while len(self.creatureSet) < self.count:
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
            while len(self.creatureSet) < self.count:
                #figuring out wherre to put it
                xMult = 1 if random.random() < 0.5 else -1
                xAug = self.spawnRadius*random.random()*TILESIZE * xMult
                x = self.x + xAug

                yMult = 1 if random.random() < 0.5 else -1
                yAug = self.spawnRadius*random.random()*TILESIZE * yMult
                y = self.y + yAug

                self.creatureSet.add(Creature(x, y, self.g1))

        else:
            while len(self.creatureSet) < self.count:
                #figuring out wherre to put it
                xMult = 1 if random.random() < 0.5 else -1
                xAug = self.spawnRadius*random.random()*TILESIZE * xMult
                x = self.x + xAug

                yMult = 1 if random.random() < 0.5 else -1
                yAug = self.spawnRadius*random.random()*TILESIZE * yMult
                y = self.y + yAug

                self.creatureSet.add(Creature(x, y))


    def repopulate(self):
        creatures = tuple(self.creatureSet)
        counter = 0
        while len(self.creatureSet) < self.count:
            counter += 1
            parent1 = random.choice(creatures)
            parent2 = random.choice(creatures)

            child = parent1.mate(parent2)

            self.creatureSet.add(child)
#            print("added", counter)
#        print("Creatures spawned:", len(self.creatureSet))


    def draw(self, canvas, color=None):
        if color is None: color = self.color
        x1 = self.x - self.size/2
        y1 = self.y + self.size/2
        x2 = self.x
        y2 = self.y - self.size/2
        x3 = self.x + self.size/2
        y3 = self.y + self.size/2

        canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill=color, width=0)

"""
Genome indexing:
0-49 reserved for attributes
rest NN weights
"""
