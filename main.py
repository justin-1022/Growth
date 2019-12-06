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
from analysis import *
import time

class Growth(App):
    def appStarted(self):
        self.isPaused = True
        self.run = True
        self.eMode = False
        self.timerDelay = 0
        self.globalAvgTracker = []
        self.tiles = []
        self.genDeathCount = [0]
        self.foods = Tile.foodSet
        for x in range(0, WIDTH, TILESIZE):
            for y in range(0, HEIGHT, TILESIZE):
                self.tiles.append(Grassland(x, y))

#        self.tiles = tuple(self.tiles)#speeds up data access and reduces ram use

        self.secondHand = 0
        self.spawnNodes = []
        #same as tiles
        self.creatures = set([])#allows for quick management w/ set funcs

        for node in self.spawnNodes:
            node.spawnCreatures()
            self.creatures = self.creatures.union(node.creatureSet)

        self.globalTopCret = None
        for c in self.creatures:
            #assigning to random cret from set to start
            self.globalTopCret = c
            break

        for tile in self.tiles:
            if tile.isViable:
                tile.spawnFood()

        self.theEditor = Editor()
        self.theAnalyzer = Analysis()

        self.iCret1 = None
        self.iCret2 = None

    def keyPressed(self, event):
        if event.key == "p":
            self.isPaused = not self.isPaused

        if event.key == "e":
            self.eMode = not self.eMode

    def mousePressed(self, event):
        #note - this would be a lot cleaner if it was inside some buttonhandling
        #function, but doing so seems like it would make passing in data difficult
        #will explore doing so in the future

        #all button handling of some form
        if self.eMode:
            Editor.selection(event.x, event.y)
            Editor.tileInsert(event.x, event.y, Editor.selected, self.tiles)
            Editor.nodeInsert(event.x, event.y, 10, len(self.globalAvgTracker),
                                                                self.spawnNodes)

        if Editor.pCreature1.isClicked:
            c1 = Editor.pCreature1.onRelease(xC=event.x, yC=event.y, creatureSet=self.creatures)
            if c1 is not None:
                if Editor.rCreature1.data != None: Editor.rCreature1.data.highlight1 = False
                Editor.rCreature1.data = c1
                Editor.rCreature1.text = ("ID=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                (c1.id, c1.fitness, int(c1.x), int(c1.y)))
                c1.highlight1 = True

        if Editor.pCreature2.isClicked:
            c2 = Editor.pCreature2.onRelease(xC=event.x, yC=event.y, creatureSet=self.creatures)
            if c2 is not None:
                if Editor.rCreature2.data != None: Editor.rCreature2.data.highlight2 = False
                Editor.rCreature2.data = c2
                Editor.rCreature2.text = ("ID=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                        (c2.id, c2.fitness, int(c2.x), int(c2.y)))
                c2.highlight2 = True

        if Editor.aNCreature1.isClicked:
            c1 = None
            Editor.aNCreature1.onRelease(creature = c1)
            if Editor.rCreature1.clickCheck(event.x, event.y):
                c1 = Editor.rCreature1.onClick()

            elif Editor.rCreature2.clickCheck(event.x, event.y):
                c1 = Editor.rCreature2.onClick()

            elif Editor.nCreature2.clickCheck(event.x, event.y):
                c1 = Editor.nCreature2.onClick()

            elif Analysis.topC.clickCheck(event.x, event.y):
                c1 = Analysis.topC.onClick()

            elif Analysis.gTopC.clickCheck(event.x, event.y):
                c1 = Analysis.gTopC.onClick()

            if c1 is not None:
                Editor.nCreature1.data = c1
                Editor.g1 = c1.genome
                Editor.nCreature1.text = "ID=%d\nFitness=%.2f" % (c1.id, c1.fitness)

        if Editor.aNCreature2.isClicked:
            c2 = None
            Editor.aNCreature2.onRelease(creature = c2)

            if Editor.rCreature1.clickCheck(event.x, event.y):
                c2 = Editor.rCreature1.onClick()

            elif Editor.rCreature2.clickCheck(event.x, event.y):
                c2 = Editor.rCreature2.onClick()

            elif Editor.nCreature2.clickCheck(event.x, event.y):
                c2 = Editor.nCreature2.onClick()

            elif Analysis.topC.clickCheck(event.x, event.y):
                c2 = Analysis.topC.onClick()

            elif Analysis.gTopC.clickCheck(event.x, event.y):
                c2 = Analysis.gTopC.onClick()

            if c2 is not None:
                Editor.nCreature2.data = c2
                Editor.g2 = c2.genome
                Editor.nCreature2.text = "ID=%d\nFitness=%.2f" % (c2.id, c2.fitness)


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
                Editor.rCreature1.text = ("ID=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                (c1.id, c1.fitness, int(c1.x), int(c1.y)))

        elif Editor.iCreature2.clickCheck(event.x, event.y):
            self.isPaused = True
            filename = filedialog.askopenfilename(initialdir="savedata/creatures")
            c2 = Editor.iCreature2.onClick(fileName=filename)
            if c2 is not None:
                Editor.rCreature2.data = c2
                Editor.rCreature2.text = ("ID=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                (c2.id, c2.fitness, int(c2.x), int(c2.y)))

        elif Editor.aNCreature1.clickCheck(event.x, event.y):
            Editor.aNCreature1.onClick()
            Editor.aNCreature2.onRelease(creature = None)

        elif Editor.aNCreature2.clickCheck(event.x, event.y):
            Editor.aNCreature2.onClick()
            Editor.aNCreature1.onRelease(creature = None)

        elif Editor.nCreature1.clickCheck(event.x, event.y):
            Editor.nCreature1.onClick()
            Editor.nCreature1.data = None
            Editor.g1 = None
            Editor.nCreature1.text = "No data"

        elif Editor.nCreature2.clickCheck(event.x, event.y):
            Editor.nCreature2.onClick()
            Editor.nCreature2.data = None
            Editor.g2 = None
            Editor.nCreature2.text = "No data"

        elif Analysis.aGens.clickCheck(event.x, event.y):
            Analysis.aGens.onClick(avgList = self.globalAvgTracker)

        elif Analysis.aNGens.clickCheck(event.x, event.y):
            nodeAvgListList = [node.avgTracker for node in self.spawnNodes]
            Analysis.aNGens.onClick(nodeAvgListList=nodeAvgListList)

        elif Analysis.mapComp.clickCheck(event.x, event.y):
            Analysis.mapComp.onClick(mapList=self.tiles)

        elif Analysis.deaths.clickCheck(event.x, event.y):
            Analysis.deaths.onClick(deathList=self.genDeathCount)

        elif Editor.pause.clickCheck(event.x, event.y):
            Editor.pause.onClick()
            self.isPaused = not self.isPaused

        elif Editor.editB.clickCheck(event.x, event.y):
            Editor.editB.onClick()
            self.eMode = not self.eMode

        elif Editor.genStep.clickCheck(event.x, event.y):
            Editor.genStep.onClick()
            self.secondHand = 499

    def mouseDragged(self, event):
        if self.eMode:
            Editor.tileInsert(event.x, event.y, Editor.selected, self.tiles)

    def mouseReleased(self, event):
        for button in Button.buttonDict.values():
            if button.isClicked and not button.wait:
                button.onRelease()

    def timerFired(self):
        if not self.isPaused:
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
    #                    print("food spawned")
            if self.secondHand % 10 == 0:
                crets = tuple(self.creatures)
                topCret = crets[0] if len(crets) > 0 else None
                for cret in crets:
                    if cret is not None:
                        if cret.fitness > topCret.fitness:
                            topCret = cret
                    if self.globalTopCret is not None:
                        if cret.fitness > self.globalTopCret.fitness:
                            self.globalTopCret = cret
                    cret.look(self.foods, 0)
                    cret.look(self.creatures, 1)

                    cret.decide()

                    cret.update(dt)
                    #realtime updating button text
                    if Editor.rCreature1.data is not None:
                        c1 = Editor.rCreature1.data
                        Editor.rCreature1.text = ("ID=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                        (c1.id, c1.fitness, int(c1.x), int(c1.y)))

                    if Editor.rCreature2.data is not None:
                        c2 = Editor.rCreature2.data
                        Editor.rCreature2.text = ("ID=%d\nFitness=%.2f\nPos=(%d, %d)" %\
                                (c2.id, c2.fitness, int(c2.x), int(c2.y)))

                    if Editor.nCreature1.data is not None:
                        c1 = Editor.nCreature1.data
                        Editor.nCreature1.text = "ID=%d\nFitness=%.2f" % (c1.id, c1.fitness)
                        Editor.g1 = c1.genome

                    if Editor.nCreature2.data is not None:
                        c2 = Editor.nCreature2.data
                        Editor.nCreature2.text = "ID=%d\nFitness=%.2f" % (c2.id, c2.fitness)
                        Editor.g2 = c2.genome

                    foodAmnt = len(Tile.foodSet)
                    Tile.foodSet = Tile.foodSet - cret.eaten
                    if foodAmnt != len(Tile.foodSet):
#                        print("foods deleted")
                        cret.eaten = set([])

                    counter = 1
                    if cret.markForDelete:
                        #removing the ones that starved
                        self.creatures.remove(cret)
                        self.genDeathCount[-1] += 1

                self.foods = Tile.foodSet

                Analysis.topC.data = topCret
                if Analysis.topC.data is not None:
                    c1 = Analysis.topC.data
                    Analysis.topC.text = "Current Top Creature\nID=%d\nFitness=%.2f" % (c1.id, c1.fitness)

                Analysis.gTopC.data = self.globalTopCret
                if Analysis.gTopC.data is not None:
                    c2 = Analysis.gTopC.data
                    Analysis.gTopC.text = "Alltime Top Creature\nID=%d\nFitness=%.2f" % (c2.id, c2.fitness)

            if self.secondHand % 500 == 0:
                self.assistedEvolution()
                self.foods = Tile.foodSet = set([])
                for tile in self.tiles:
                    if tile.isViable: tile.spawnFood()

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
#            if not self.isPaused:
#                print(count, len(self.creatures), len(tt))
            population[i].draw(canvas)

        self.theEditor.draw(canvas)
        self.theAnalyzer.draw(canvas)

        for button in Button.buttonDict.values():
            button.draw(canvas)

        if self.eMode:
            for node in self.spawnNodes:
                node.draw(canvas)

#        print([cret.id for cret in self.creatures])

    def assistedEvolution(self):
        globalAvg = 0
        for node in self.spawnNodes:

            #refilling to node capacity
            if len(node.creatureSet) > 1:
                #removing the unfit and updating masterset
                newCreatureSet, avgFitness = Genetics.luckSelector(node.creatureSet)
                deletedCrets = node.creatureSet - newCreatureSet
                node.creatureSet = newCreatureSet
                self.creatures = self.creatures - deletedCrets
                node.repopulate()


            else:
                #just refilling for emptyish nodes
                node.spawnCreatures()
                avgFitness = 0

            node.avgTracker.append(avgFitness)
            node.startGen = len(self.globalAvgTracker)
            globalAvg += avgFitness

            #updating masterset
            self.creatures = self.creatures.union(node.creatureSet)

        globalAvg /= len(self.spawnNodes)
        self.globalAvgTracker.append(globalAvg)
        self.genDeathCount.append(0)
#                print(len(self.creatures), len(node.creatureSet))

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
