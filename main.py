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
from button import *
import time

class Growth(App):
    def appStarted(self):
        self.pause = True
        self.run = True
        self.eMode = True
        self.noEdit = False #fixes bug where filedialog triggers mouseDragged
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

        self.iCret1 = None
        self.iCret2 = None

    def keyPressed(self, event):
        if event.key == "p":
            self.pause = not self.pause

        if event.key == "e":
            self.eMode = not self.eMode

    def mousePressed(self, event):
        #note - this would be a lot cleaner if it was inside some buttonhandling
        #function, but doing so seems like it would make passing in data difficult
        #will explore doing so in the future
        if self.eMode:
            Editor.selection(event.x, event.y)
            Editor.tileInsert(event.x, event.y, Editor.selected, self.tiles)
            Editor.nodeInsert(event.x, event.y, 10, self.spawnNodes)

        if Editor.pCreature1.isClicked:
            c1 = Editor.pCreature1.onRelease(xC=event.x, yC=event.y, creatureSet=self.creatures)
            if c1 is not None:
                if Editor.rCreature1.data != None: Editor.rCreature1.data.highlight1 = False
                Editor.rCreature1.data = c1
                Editor.rCreature1.text = ("Id=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                (c1.id, c1.fitness, int(c1.x), int(c1.y)))
                c1.highlight1 = True

        if Editor.pCreature2.isClicked:
            c2 = Editor.pCreature2.onRelease(xC=event.x, yC=event.y, creatureSet=self.creatures)
            if c2 is not None:
                if Editor.rCreature2.data != None: Editor.rCreature2.data.highlight2 = False
                Editor.rCreature2.data = c2
                Editor.rCreature2.text = ("Id=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                        (c2.id, c2.fitness, int(c2.x), int(c2.y)))
                c2.highlight2 = True

        if Editor.iMap.clickCheck(event.x, event.y):
            self.isPaused =  True
            filename = filedialog.askopenfilename(initialdir="savedata/maps")
            loadedMap = Editor.iMap.onClick(fileName=filename)
            if loadedMap is not None:
                self.tiles = loadedMap
            self.mouseReleased(event)

        elif Editor.sMap.clickCheck(event.x, event.y):
            self.isPaused = True
            filename = filedialog.asksaveasfilename(initialdir="savedata/maps")
            Editor.sMap.onClick(mapList = self.tiles, fileName=filename)
            self.mouseReleased(event)

        elif Editor.pCreature1.clickCheck(event.x, event.y):
            Editor.pCreature1.onClick()

        elif Editor.pCreature2.clickCheck(event.x, event.y):
            Editor.pCreature2.onClick()

        elif Editor.sCreature1.clickCheck(event.x, event.y):
            self.isPaused = True
            if Editor.rCreature1.data != None:
                c1 = Editor.rCreature1.data
                filename = filedialog.asksaveasfilename(initialdir="savedata/creatures")
                Editor.sCreature1.onClick(fileName=filename, creature=c1)

        elif Editor.sCreature2.clickCheck(event.x, event.y):
            self.isPaused = True
            if Editor.rCreature2.data != None:
                c2 = Editor.rCreature2.data
                filename = filedialog.asksaveasfilename(initialdir="savedata/creatures")
                Editor.sCreature2.onClick(fileName=filename, creature=c2)

        elif Editor.iCreature1.clickCheck(event.x, event.y):
            self.isPaused = True
            filename = filedialog.askopenfilename(initialdir="savedata/creatures")
            c1 = Editor.iCreature1.onClick(fileName=filename)
            if c1 is not None:
                Editor.rCreature1.data = c1
                Editor.rCreature1.text = ("Id=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                (c1.id, c1.fitness, int(c1.x), int(c1.y)))

        elif Editor.iCreature2.clickCheck(event.x, event.y):
            self.isPaused = True
            filename = filedialog.askopenfilename(initialdir="savedata/creatures")
            c2 = Editor.iCreature2.onClick(fileName=filename)
            if c2 is not None:
                Editor.rCreature2.data = c2
                Editor.rCreature2.text = ("Id=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                (c2.id, c2.fitness, int(c2.x), int(c2.y)))

    def mouseDragged(self, event):
        if self.eMode:
            Editor.tileInsert(event.x, event.y, Editor.selected, self.tiles)

    def mouseReleased(self, event):
        self.noEdit = False
        for button in Button.buttonDict.values():
            if button.isClicked and not button.wait:
                button.onRelease()

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
                    if Editor.rCreature1.data is not None:
                        c1 = Editor.rCreature1.data
                        Editor.rCreature1.text = ("Id=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                        (c1.id, c1.fitness, int(c1.x), int(c1.y)))

                    if Editor.rCreature2.data is not None:
                        c2 = Editor.rCreature2.data
                        Editor.rCreature2.text = ("Id=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                (c2.id, c2.fitness, int(c2.x), int(c2.y)))

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

        self.theEditor.draw(canvas)

        if self.eMode:
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
    -[COMPLETE]select different envionment tiles and paint them with mouse
    -[COMPLETE]place spawn nodes anywhere
    -[DEBUG+UI]import creatures from text file
    -design custom creature genomes in friendly format
analytics
    -display graphs with average age, average fitness over time
    -display top performer
export/import creatures
    -[DEBUG+UI]send genomes to text file
    -[DEBUG+UI]receive genomes from text file
    -can import one to node for clones, two for parents
    -can import individual creature to node
export/import maps
    -[DEBUG+UI]save tile list to txt file
    -[DEBUG+UI]read from txt file to list
"""



Growth(width=ALLWIDTH, height=ALLHEIGHT)
