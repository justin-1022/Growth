#This file will handle the analysis mode of the app
#displays graphics, allows one to view genomes, top performers, etc
from header import *
from environment import *
from creature import *
class DataManagement:

    @staticmethod
    def importMap(fileName):
        filePath = "savedata/%s"%fileName
        saveFile = open(filePath, "r")

        tileString = savefile.readline().strip().rstrip("-")
        viabilityString = savefile.readline().strip().rstrip("-")

        tileList = tileString.split("-")
        viabiltyList = viabilityString.split("-")
        viabiltyList = [float(n) for n in viabiltyList]

        mapList = []
        for i in range(len(tileList)):
            #figuring out where this tile is supposed to be
            tileType = tileList[i]
            tileX, tileY = Editor.tilePosFind(i)
            xC, yC = tileX * TILESIZE, tileY * TILESIZE

            if tileType == "grassland":
                newTile = Grassland(xC, yC)

            elif tileType == "savanna":
                newTile = Savanna(xC, yC)

            elif tileType == "marsh":
                newTile = Marsh(xC, yC)

            elif tileType == "forest":
                newTile = Forest(xC, yC)

            elif tileType == "desert":
                newTile = Desert(xC, yC)

            #recomputing viability to match save data
            newTile.viability = viabiltyList[i]
            newTile.isViable = newTile.viability > newTile.threshold

            mapList.append(newTile)

        saveFile.close()
        return mapList


    @staticmethod
    def saveMap(mapList, fileName):
        filePath = "savedata/%s"%fileName
        saveFile = open(filePath, "w")

        mapString = ""
        viabilityString = ""
        for tile in mapList:
            if isinstance(tile, Grassland):
                mapString += "grassland-"

            elif isinstance(tile, Savanna):
                mapString += "savanna-"

            elif isinstance(tile, Marsh):
                mapString += "marsh-"

            elif isinstance(tile, Forest):
                mapString += "forest-"

            elif isinstance(tile, Desert):
                mapString += "desert-"

            viabilityString += "%.2f-" % tile.viability

        savefile.write(mapString + "\n" + viabilityString)
        saveFile.close()

    @staticmethod
    def importCreature(fileName):
        filePath = "savedata/%s"%fileName
        saveFile = open(filePath, "r")

        fitness = float(saveFile.readline().strip())
        genome = np.array(saveFile.readline.strip().split("-"))

        return fitness, genome

    @staticmethod
    def saveCreature(creature, fileName):
        filePath = "savedata/%s"%fileName
        saveFile = open(filePath, "w")

        creatureString = ""

        creatureString += "%.2f\n" % creature.viability
        creatureString += "-".join(creature.genome)

        saveFile.write(creatureString)
        saveFile.close()

    @staticmethod
    def importNode(fileName):
        #send to list that will supply other functons with creatures
        return node
        
    @staticmethod
    def saveNode(node, fileName):
        pass

"""
nodes
    file1
        '
        avgFitness
        creature1 genome...
        creatureN genome

        '
    file2
    fileN
creatures
    file1 <- Name
        '
        fitness
        genome
        '
    file2
    fileN

"""
