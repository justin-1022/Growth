#This file will handle the analysis mode of the app
#displays graphics, allows one to view genomes, top performers, etc
from header import *
from environment import *
from creature import *

class DataManagement:

    @staticmethod
    def importMap(fileName):
        filePath = fileName
        try:
            saveFile = open(filePath, "r")

            tileString = saveFile.readline().strip().rstrip("-")
            viabilityString = saveFile.readline().strip().rstrip("-")

            tileList = tileString.split("-")
            viabiltyList = viabilityString.split("-")
            viabiltyList = [float(n) for n in viabiltyList]

            mapList = []
            for i in range(len(tileList)):
                #figuring out where this tile is supposed to be
                tileType = tileList[i]
                tileX, tileY = tilePosFind(i)
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

        except Exception:
            return None


    @staticmethod
    def saveMap(mapList, fileName):
        filePath = fileName
        try:
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

            saveFile.write(mapString + "\n" + viabilityString)
            saveFile.close()

        except Exception:
            return None

    @staticmethod
    def importCreature(fileName):
        filePath = fileName
        saveFile = open(filePath, "r")

        fitness = float(saveFile.readline().strip())

        genome = (saveFile.readline().strip().split("-"))
        genome =  np.array([float(n) for n in genome])

        loadedCret = Creature(WIDTH/2, HEIGHT/2, genome)
        loadedCret.fitness = fitness

        return loadedCret

    @staticmethod
    def saveCreature(creature, fileName):
        filePath = fileName
        saveFile = open(filePath, "w")

        creatureString = ""
        genomeList = [str(n) for n in list(creature.genome)]

        creatureString += "%.2f\n" % creature.fitness
        creatureString += "-".join(genomeList)

        saveFile.write(creatureString)
        saveFile.close()

    @staticmethod
    def importNode(fileName):
        #send to list that will supply other functons with creatures
        return node

    @staticmethod
    def saveNode(node, fileName):
        pass

    @staticmethod
    def pickCreature(xC, yC, creatureSet):
        for creature in creatureSet:
            if creature.clickCheck(xC, yC):
                return creature


def tilePosFind(i):
    #returns tile coordinates NOT absolute coordinates
    return i//(HEIGHT//TILESIZE), i%(HEIGHT//TILESIZE)

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
