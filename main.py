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



    @staticmethod
    def tileFind(tiles, x, y):
        xInc = WIDTH//TILESIZE

        return tiles[xInc*x+y]

    def keyPressed(self, event):
        pass

    def timerFired(self):
        self.secondHand += 1
        print(self.secondHand)
        dt = self.tick()
        """
        if self.secondHand == 1:
            self.start = time.time()

        if self.secondHand == 100:
            self.end = time.time()
            input(abs(self.start-self.end)/10)"""

        if self.secondHand > 1000: self.secondHand = 1

        if self.secondHand % 100 == 0:
            for tile in self.tiles:
                if tile.isViable:
                    tile.spawnFood()
                    print("food spawned")

        if self.secondHand % 10 == 0:
            for cret in self.creatures:
                cret.look(self.foods, 0)
                cret.look(self.creatures, 1)

                cret.update(dt)


    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, self.width, self.height, fill="grey")
        for tile in self.tiles:
            tile.draw(canvas)

        for food in self.foods:
            food.draw(canvas)

        for creature in self.creatures:
            creature.draw(canvas)



Growth(width=WIDTH, height=HEIGHT)
