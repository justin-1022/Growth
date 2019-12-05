#level editor mode
from header import *
import paintcan
from environment import *
from creature import *
from datamgmt import *
from button import *

class Editor:
    #this class is UgLy!!!, but it works lol
    #me in the future (or TA reading this) - you might want to get some tea first
    #the tileBox and related functions were made before general button class
    #so they are currently inconsistent with predominant logic
    #note - (xC, yC) is real coordinate, (x, y) is tile grid coordinate
    selected = "forest"
    tileTypes = ["grassland", "forest", "desert", "savanna", "marsh"]
    spacing = 15
    thinSpacing = 10
    pickSize = 30

    tileBox = (spacing, HEIGHT + spacing*1.5)#top left corner
    tileBoxWidth = pickSize*2 + spacing*3
    tileBoxHeight = pickSize*3 + spacing*4

    #display tiles/node with relative locations
    tiles = [Grassland(spacing, spacing),#placeholder tiles for selection/drawing
            Forest(spacing*2 + pickSize, spacing),
            Desert(spacing, spacing*2 + pickSize),
            Savanna(spacing*2 + pickSize, spacing*2 + pickSize),
            Marsh(spacing, spacing*3 + pickSize*2)]

    node = SpawnNode(spacing*2 + pickSize/2 + pickSize,
                        spacing*3 + pickSize*2 + pickSize/2, 0)

    #putting things in the box
    for tile in tiles:
        tile.x += tileBox[0]
        tile.y += tileBox[1]
        tile.size = pickSize
        tile.viability = 0

    node.x += tileBox[0]
    node.y += tileBox[1]
    node.size = pickSize

    #map box
    mapBox = (tileBox[0] + tileBoxWidth + thinSpacing, tileBox[1])
    mapBoxWidth = pickSize*4 + thinSpacing*3
    mapBoxHeight = pickSize + thinSpacing*2

    sMapTxt = "Save Map"
    sMap = Button(mapBox[0] + thinSpacing, mapBox[1] + thinSpacing, pickSize*2,
                pickSize, DataManagement.saveMap, "sMap", sMapTxt)

    iMapTxt = "Load Map"
    iMap = Button(mapBox[0] + thinSpacing*2 + pickSize*2, mapBox[1] + thinSpacing,
            pickSize*2, pickSize, DataManagement.importMap, "iMap", iMapTxt)

    #creature import export box
    cBox = (mapBox[0] + mapBoxWidth + thinSpacing, mapBox[1])
    cBoxWidth = pickSize*10 + thinSpacing*4
    cBoxHeight = thinSpacing*3 + pickSize*4

    iCreatureTxt = "Load\nCreature"
    sCreatureTxt = "Save\n<-"
    pCreatureTxt = "Pick\nCreature"
    iCreature1 = Button(cBox[0] + thinSpacing, cBox[1] + thinSpacing, pickSize*2,
    pickSize, DataManagement.importCreature, "iCreature1", iCreatureTxt + "(1)")

    sCreature1 = Button(cBox[0] + thinSpacing*3 + pickSize*9, cBox[1] + thinSpacing,
            pickSize, pickSize*2, DataManagement.saveCreature, "sCreature1", sCreatureTxt + "(1)")

    pCreature1 = Button(cBox[0] + thinSpacing, cBox[1] + thinSpacing + pickSize,
            pickSize*2, pickSize, DataManagement.pickCreature, "pCreature1", pCreatureTxt + "(1)", True)

    rCreature1 = DataButton(cBox[0] + thinSpacing*2 + pickSize*2, cBox[1] + thinSpacing,
            pickSize*7, pickSize*2, None, "rCreature1")

    iCreature2 = Button(cBox[0] + thinSpacing, cBox[1] + thinSpacing*2 + pickSize*2,
            pickSize*2, pickSize, DataManagement.importCreature, "iCreature2", iCreatureTxt + "(2)")

    sCreature2 = Button(cBox[0] + thinSpacing*3 + pickSize*9, cBox[1] + thinSpacing*2 + pickSize*2,
            pickSize, pickSize*2, DataManagement.saveCreature, "sCreature2", sCreatureTxt + "(2)")

    pCreature2 = Button(cBox[0] + thinSpacing, cBox[1] + thinSpacing*2 + pickSize*3,
            pickSize*2, pickSize, DataManagement.pickCreature, "pCreature2", pCreatureTxt + "(2)", True)

    rCreature2 = DataButton(cBox[0] + thinSpacing*2 + pickSize*2,
            cBox[1] + thinSpacing*2 + pickSize*2, pickSize*7, pickSize*2, None, "rCreature2")

    #node insertion box
    nodeBox = (mapBox[0], mapBox[1] + mapBoxHeight + thinSpacing)
    nodeBoxWidth = thinSpacing*3 + pickSize*4
    nodeBoxHeight = thinSpacing*3 + pickSize*2
    aNCreatureTxt = "add->"

    aNCreature1 = Button(nodeBox[0] + thinSpacing, nodeBox[1] + thinSpacing,
                pickSize, pickSize, DataManagement.addCreature, "aNCreature1",
                aNCreatureTxt, True)

    aNCreature2 = Button(nodeBox[0] + thinSpacing, nodeBox[1] + thinSpacing*2 + pickSize,
                pickSize, pickSize, DataManagement.addCreature, "aNCreature2",
                aNCreatureTxt, True)

    nCreature1 = DataButton(nodeBox[0] + thinSpacing*2 + pickSize, nodeBox[1] + thinSpacing,
                pickSize*3, pickSize, None, "nCreature1")

    nCreature2 = DataButton(nodeBox[0] + thinSpacing*2 + pickSize,
        nodeBox[1] + thinSpacing*2 + pickSize, pickSize*3, pickSize, None, "nCreature2")

    g1 = None
    g2 = None

    def __init__(self):
        pass

    def pickCreature(self):
        pass

    def draw(self, canvas):
        #tile selection stuff

        #tile box
        canvas.create_rectangle(Editor.tileBox[0], Editor.tileBox[1],
        Editor.tileBox[0] + Editor.tileBoxWidth,
        Editor.tileBox[1] + Editor.tileBoxHeight, fill="darkgrey")

        #selection highlighting
        #currently selected tile from tiles(not tiletypes)
        if Editor.selected != "node":
            theTile = Editor.tiles[Editor.tileTypes.index(Editor.selected)]
            showSpace = Editor.pickSize * 0.2
            canvas.create_rectangle(theTile.x - showSpace, theTile.y - showSpace,
                theTile.x + theTile.size + showSpace,
                theTile.y + theTile.size + showSpace,
                fill=paintcan.toHex(paintcan.yellow))

        else:
            showSpace = Editor.pickSize * 0.2
            theNode = Editor.node
            canvas.create_rectangle(theNode.x - theNode.size/2 - showSpace,
            theNode.y - theNode.size/2 - showSpace,
                theNode.x + theNode.size/2 + showSpace,
                theNode.y + theNode.size/2 + showSpace,
                fill=paintcan.toHex(paintcan.yellow))


        #actual tiles to pick
        for tile in Editor.tiles:
            tile.draw(canvas)

        #node stuff
        Editor.node.draw(canvas)

        #map import export box
        canvas.create_rectangle(Editor.mapBox[0], Editor.mapBox[1],
        Editor.mapBox[0] + Editor.mapBoxWidth,
        Editor.mapBox[1] + Editor.mapBoxHeight, fill="darkgrey")

        #creature import export and select box
        canvas.create_rectangle(Editor.cBox[0], Editor.cBox[1],
        Editor.cBox[0] + Editor.cBoxWidth,
        Editor.cBox[1] + Editor.cBoxHeight, fill="darkgrey")

        #node box
        canvas.create_rectangle(Editor.nodeBox[0], Editor.nodeBox[1],
        Editor.nodeBox[0] + Editor.nodeBoxWidth,
        Editor.nodeBox[1] + Editor.nodeBoxHeight, fill="darkgrey")

        for button in Button.buttonDict.values():
            button.draw(canvas)

    @staticmethod
    def coordConvert(xC, yC):
        tileX = xC//TILESIZE
        tileY = yC//TILESIZE

        return tileX, tileY

    @staticmethod
    def selection(xC, yC):
        for i in range(len(Editor.tiles)):
            tile = Editor.tiles[i]
            if (xC >= tile.x and xC <= tile.x + tile.size and
                yC >= tile.y and yC <= tile.y + tile.size):

                Editor.selected = Editor.tileTypes[i]

        node = Editor.node
        if (xC >= node.x - node.size/2 and xC <= node.x + node.size/2 and
            yC >= node.y - node.size/2 and yC <= node.y + node.size/2):
            Editor.selected = "node"

    @staticmethod
    def tileInsert(xC, yC, tileType, tileList):
        if xC > WIDTH or yC > HEIGHT: return None#checking bounds
        if tileType == "node": return None

        x, y = Editor.coordConvert(xC, yC)
        inSpot = tileList[Editor.tileFind(x, y)]
        if tileType == "grassland":
            tileList[Editor.tileFind(x, y)] = Grassland(inSpot.x, inSpot.y)

        elif tileType == "forest":
            tileList[Editor.tileFind(x, y)] = Forest(inSpot.x, inSpot.y)

        elif tileType == "desert":
            tileList[Editor.tileFind(x, y)] = Desert(inSpot.x, inSpot.y)

        elif tileType == "savanna":
            tileList[Editor.tileFind(x, y)] = Savanna(inSpot.x, inSpot.y)

        elif tileType == "marsh":
            tileList[Editor.tileFind(x, y)] = Marsh(inSpot.x, inSpot.y)

    def nodeInsert(xC, yC, count, nodeList):
        g1 = Editor.g1
        g2 = Editor.g2
        print(g1 is None, g2 is None)
        if Editor.selected != "node": return None
        if xC > WIDTH or yC > HEIGHT: return None
        nodeList.append(SpawnNode(xC, yC, count, g1, g2))

    @staticmethod
    def tileFind(x, y):
        xInc = HEIGHT//TILESIZE

        return xInc*x+y

    @staticmethod
    def tilePosFind(i):
        #returns tile coordinates NOT absolute coordinates
        return i//(HEIGHT//TILESIZE), i%(HEIGHT//TILESIZE)
