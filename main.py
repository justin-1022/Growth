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
from editor import *
import time

class Growth(App):
    def appStarted(self):
        self.pause = True
        self.run = True
        self.eMode = True
        self.timerDelay = 0
        self.scrollX = 0
        self.scrollMargin = 50
        self.tiles = []
        self.foods = Tile.foodSet
        for x in range(0, WIDTH, TILESIZE):
            for y in range(0, HEIGHT, TILESIZE):
                self.tiles.append(Grassland(x, y))

#        self.tiles = tuple(self.tiles)#speeds up data access and reduces ram use

        self.secondHand = 0
        self.spawnNodes = [SpawnNode(WIDTH/2, HEIGHT/2, 10)]
        #same as tiles
        self.creatures = set([])#allows for quick management w/ set funcs

        for node in self.spawnNodes:
            node.spawnCreatures()
            self.creatures = self.creatures.union(node.creatureSet)

        for tile in self.tiles:
            if tile.isViable:
                tile.spawnFood()

        self.theEditor = Editor()

    def keyPressed(self, event):
        if event.key == "p":
            self.pause = not self.pause

        if event.key == "e":
            self.eMode = not self.eMode

    def mousePressed(self, event):
        if self.eMode:
            Editor.selection(event.x, event.y)
            Editor.tileInsert(event.x, event.y, Editor.selected, self.tiles)
            Editor.nodeInsert(event.x, event.y, 10, self.spawnNodes)


    def mouseDragged(self, event):
        if self.eMode:
            Editor.tileInsert(event.x, event.y, Editor.selected, self.tiles)


    def timerFired(self):
        if not self.pause:
            self.secondHand += 1
#            print(self.secondHand)
            dt = self.tick()
            """
            if self.secondHand == 1:
                self.start = time.time()

            if self.secondHand == 100:
                self.end = time.time()
                input(abs(self.start-self.end)/10)"""

            if self.secondHand > 1000: self.secondHand = 1

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

                    foodAmnt = len(Tile.foodSet)
                    Tile.foodSet = Tile.foodSet - cret.eaten
                    if foodAmnt != len(Tile.foodSet):
                        print("foods deleted")
                        cret.eaten = set([])

                    counter = 1
                    if cret.markForDelete:
                        pass
#                        print("deleted", (counter))
#                        self.creatures.remove(cret)

                self.foods = Tile.foodSet

            if self.secondHand % 500 == 0:
                self.assistedEvolution()

    def redrawAll(self, canvas):
        canvas.create_rectangle(0, 0, ALLWIDTH, ALLHEIGHT, fill="grey")
        for tile in self.tiles:
            tile.draw(canvas)

        for food in self.foods:
            food.draw(canvas)

        count = 0
        population = tuple(self.creatures)
        for i in range(len(population)):
            count += 1
#            if not self.pause:
#                print(count, len(self.creatures), len(tt))
            population[i].draw(canvas)

        if self.eMode:
            self.theEditor.draw(canvas)

            for node in self.spawnNodes:
                node.draw(canvas)

#        print([cret.id for cret in self.creatures])

    def assistedEvolution(self):
            for node in self.spawnNodes:


                #refilling to node capacity
                if len(node.creatureSet) > 1:
                    #removing the unfit and updating masterset
                    newCreatureSet = Genetics.luckSelector(node.creatureSet)
                    deletedCrets = node.creatureSet - newCreatureSet
                    node.creatureSet = newCreatureSet
                    self.creatures = self.creatures - deletedCrets
                    node.repopulate()

                else:
                    #just refilling for emptyish nodes
                    node.spawnCreatures()

                #updating masterset
                self.creatures = self.creatures.union(node.creatureSet)
                print(len(self.creatures), len(node.creatureSet))

    def editor(self):
        #edit environment tiles(list insert/deletions)

        #edit spawn nodes

        #directly inject a creature into node

        #create spawn nodes random or with imported parent(s)

        #should be able to edit whenever
        pass

    def viewTables(self):
        #read saved avgFitness scores from file

        #plot avg Fitness vs generations (time)

        #plot current fitness distribution by spawn node and by creature
        #in each spawn node

        #display top performing creature in mini window
        pass



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



Growth(width=ALLWIDTH, height=ALLHEIGHT)
