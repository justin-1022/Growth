#handling data analysis related buttons and plotting functions
from header import *
from editor import *
import matplotlib.pyplot as plt

def avgOverGens(avgList):
    plt.clf()
    genList = range(len(avgList))
    plt.plot(genList, avgList, "ro", genList, avgList)
    plt.xticks(genList)
    plt.xlabel("Generation Number")
    plt.ylabel("Global Average Fitness")
    plt.title("Global Average Fitness Over Time")

    plt.show(block=False)

def nodeAvgOverGens(nodeAvgListList):
    plt.clf()
    colorList = ["r", "b", "k", "g", "y"]
    genList = range(len(nodeAvgListList[0]))
    for nodeAvgList in nodeAvgListList:
        plt.plot(genList, nodeAvgList, random.choice(colorList))

    plt.xticks(genList)

    plt.xlabel("Generation Number")
    plt.ylabel("Average Fitness")
    plt.title("Average Fitness Over Time by Node")

    plt.show(block=False)

def mapComp(mapList):
    labels = ["Grassland", "Forest", "Savanna", "Desert", "Marsh"]
    plt.clf()
    counterList = [0, 0, 0, 0, 0]

    for tile in mapList:
        if isinstance(tile, Grassland):
            counterList[0] += 1

        elif isinstance(tile, Savanna):
            counterList[2] += 1

        elif isinstance(tile, Marsh):
            counterList[4] += 1

        elif isinstance(tile, Forest):
            counterList[1] += 1

        elif isinstance(tile, Desert):
            counterList[3] += 1

    popCount = 0
    for i in range(len(counterList)):
        if counterList[i-popCount] == 0:
            counterList.pop(i-popCount)
            labels.pop(i-popCount)
            popCount += 1

    plt.pie(counterList, labels=labels, autopct='%1.1f%%')
    plt.title("Map Biome Distribution")
    plt.show(block=False)

def numDeaths(deathList):
    plt.clf()
    genList = range(len(deathList))

    plt.plot(genList, deathList, "ro", genList, deathList)
    plt.xticks(genList)
    plt.xlabel("Generation Number")
    plt.ylabel("Death Count")
    plt.title("Deaths By Starvation Over Time")

    plt.show(block=False)


class Analysis:
    spacing = Editor.spacing
    thinSpacing = Editor.thinSpacing
    pickSize = Editor.pickSize

    aBox = (Editor.cBox[0] + Editor.cBoxWidth + thinSpacing, Editor.cBox[1])
    aBoxWidth = thinSpacing*3 + pickSize*8
    aBoxHeight = thinSpacing*3 + pickSize*4

    aGens = Button(aBox[0] + thinSpacing, aBox[1] + thinSpacing, pickSize*2, pickSize,
                    avgOverGens, "aGens", "plot avg\nFitness")

    aNGens = Button(aBox[0] + thinSpacing, aBox[1] + thinSpacing*2 + pickSize,
        pickSize*2, pickSize, nodeAvgOverGens, "aNGens", "plot avg\nNode Fitness")

    mapComp = Button(aBox[0] + thinSpacing*2 + pickSize*2, aBox[1] + thinSpacing,
        pickSize*2, pickSize, mapComp, "mapComp", "plot map\nDistribution")

    deaths = Button(aBox[0] + thinSpacing*2 + pickSize*2, aBox[1] + thinSpacing*2 + pickSize,
        pickSize*2, pickSize, numDeaths, "deaths", "plot \nDeath Count")

    topC = DataButton(aBox[0] + thinSpacing, aBox[1] + thinSpacing*3 + pickSize*2,
        pickSize*4, pickSize*2-thinSpacing, None, "topC")

    gTopC = DataButton(aBox[0] + thinSpacing*2 + pickSize*4, aBox[1] + thinSpacing*3 + pickSize*2,
        pickSize*4, pickSize*2-thinSpacing, None, "gTopC")

    def __init__(self):
        pass

    def draw(self, canvas):
        #analysis box(duh)
        canvas.create_rectangle(Analysis.aBox[0], Analysis.aBox[1],
        Analysis.aBox[0] + Analysis.aBoxWidth,
        Analysis.aBox[1] + Analysis.aBoxHeight, fill="darkgrey")
