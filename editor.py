#level editor mode
from header import *
import paintcan
from environment import *
from creature import *

class Editor:
    #note - (xC, yC) is real coordinate, (x, y) is tile grid coordinate
    selected = "forest"
    tileTypes = ["grassland", "forest", "desert", "savanna", "marsh"]
    spacing = 15
    selectionSize = 30

    tileBox =  (spacing*2, HEIGHT + spacing*2)#top left corner
    boxWidth = selectionSize*2 + spacing*3
    boxHeight = selectionSize*3 + spacing*4

    #display tiles/node with relative locations
    tiles = [Grassland(spacing, spacing),#placeholder tiles for selection/drawing
            Forest(spacing*2 + selectionSize, spacing),
            Desert(spacing, spacing*2 + selectionSize),
            Savanna(spacing*2 + selectionSize, spacing*2 + selectionSize),
            Marsh(spacing, spacing*3 + selectionSize*2)]

    node = SpawnNode(spacing*2 + selectionSize/2 + selectionSize,
                        spacing*3 + selectionSize*2 + selectionSize/2, 0)

    #putting things in the box
    for tile in tiles:
        tile.x += tileBox[0]
        tile.y += tileBox[1]
        tile.size = selectionSize
        tile.viability = 0

    node.x += tileBox[0]
    node.y += tileBox[1]
    node.size = selectionSize


    def __init__(self):
        pass

    def draw(self, canvas):
        #tile selection stuff

        #tile box
        canvas.create_rectangle(Editor.tileBox[0], Editor.tileBox[1],
        Editor.tileBox[0] + Editor.boxWidth,
        Editor.tileBox[1] + Editor.boxHeight, fill="darkgrey")

        #selection highlighting
        #currently selected tile from tiles(not tiletypes)
        if Editor.selected != "node":
            theTile = Editor.tiles[Editor.tileTypes.index(Editor.selected)]
            showSpace = Editor.selectionSize * 0.2
            canvas.create_rectangle(theTile.x - showSpace, theTile.y - showSpace,
                theTile.x + theTile.size + showSpace,
                theTile.y + theTile.size + showSpace,
                fill=paintcan.toHex(paintcan.yellow))

        else:
            showSpace = Editor.selectionSize * 0.2
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

    def nodeInsert(xC, yC, count, nodeList, g1=None, g2=None):
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
