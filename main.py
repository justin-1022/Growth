#this will handle the actual simulation part of the project
#will be a large top down world with basic shapes for creatures
#creatures move, gather resources, etc
#different environmental factors can be introduced or levels created


#add things like lightening strikes, forest fires, floods, etc
#specify how many years before that thing happens
#player setup allows for full planning phase where they decide
#when in the simulation all these future events will happen and see how
#the creatures respond
from CmU_112_GrApHiCs import *
from tkinter import *
from header import *
from environment import *
from creature import *
from genetics import *
import time

class Growth(App):
    def appStarted(self):
        self.timerDelay = 0
        self.scrollX = 0
        self.scrollMargin = 50
        self.tiles = []
        self.foods = Tile.foodList
        for x in range(0, self.width, TILESIZE):
            for y in range(0, self.height, TILESIZE):
                self.tiles.append(Grassland(x, y))

        self.secondHand = 0
        self.spawnNodes = [spawnNode(self.width/2, self.height/2, 10)]
        self.creatures = set([])

        for node in self.spawnNodes:
            node.spawnCreatures()
            self.creatures = self.creatures.union(node.creatureSet)

        for tile in self.tiles:
            if tile.isViable:
                tile.spawnFood()

    @staticmethod
    def tileFind(tiles, x, y):
        xInc = WIDTH//TILESIZE

        return tiles[xInc*x+y]

    def keyPressed(self, event):
        pass

    def timerFired(self):
        self.secondHand += 1
#        print(self.secondHand)
        dt = self.tick()
        """
        if self.secondHand == 1:
            self.start = time.time()

        if self.secondHand == 100:
            self.end = time.time()
            input(abs(self.start-self.end)/10)"""

        if self.secondHand > 5000: self.secondHand = 1

        if self.secondHand == 5000:
            for tile in self.tiles:
                if tile.isViable:
                    tile.spawnFood()

            for cret in self.creatures:
                cret.safe = False
#                    print("food spawned")

        if self.secondHand % 10 == 0:
            for cret in tuple(self.creatures):
                cret.look(self.foods, 0)
                cret.look(self.creatures, 1)

                cret.decide()

                cret.update(dt)
                if cret.markForDelete:
                    self.creatures.remove(cret)

        if self.secondHand == 1000:
            self.assistedEvolution()

    def keyPressed(self, event):
        if event.key == "p":
            for cret in self.creatures:
                print(cret.genome)

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill="grey")
        for tile in self.tiles:
            tile.draw(canvas)

        for food in self.foods:
            food.draw(canvas)

        for creature in self.creatures:
            creature.draw(canvas)

    def assistedEvolution(self):
        if len(self.creatures) > 1:
            self.creatures = Genetics.luckSelector(self.creatures)

            for node in self.spawnNodes:
                node.creatureSet = node.creatureSet.intersection(self.creatures)
                node.repopulate()

                self.creatures = self.creatures.union(node.creatureSet)
                print(len(self.creatures), len(node.creatureSet))

        else:
            for node in self.spawnNodes:
                node.creatureSet = node.creatureSet.intersection(self.creatures)
                node.spawnCreatures()

                self.creatures = self.creatures.union(node.creatureSet)
                print(len(self.creatures), len(node.creatureSet))


#EDITOR FEATURES:
"""
select different envionment tiles and paint them with mouse
place spawn nodes anywhere
import creatures from text file
design custom creature genomes in friendly format
"""

"""
features to add to make this DONE:
editor(see above)
    -select different envionment tiles and paint them with mouse
    -place spawn nodes anywhere
    -import creatures from text file
    -design custom creature genomes in friendly format
analytics
    -display graphs with average age, average fitness over time
    -display top performer
export/import creatures
    -send genomes to text file
    -receive genomes from text file
    -can import one to node for clones, two for parents
    -can import individual creature to node
export/import maps
    -save tile list to txt file
    -read from txt file to list
"""



Growth(width=WIDTH, height=HEIGHT)
