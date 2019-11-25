#graphics subclassing
from header import *
from tkinter import *

class Tile:
    #basic biome tile - never use this, subclass
    foodList = []
    def __init__(self, x, y, size=TILESIZE):
        #for drawing
        self.size = size
        self.x = x#top left corner
        self.y = y
        self.color = "pink"

        #tile food properties
        self.viability = random.random()
        self.threshold = 0 #threshold for food viability so
        #food will spawn in nearby area
        self.isViable = self.viability < self.threshold
        self.foodChance = 1 #food overall spawn chance
        self.foodBook = None #dict of proportional food type spawn rates
        self.foodRadius = 1 #radius food spawns in

        #multipliers for creatures travelling here
        self.speedMult = 1
        self.soundMult = 1
        self.visMult = 1
        self.fatigueMult = 1

    def draw(self, canvas, color=None):
        if color is None: color = self.color

        canvas.create_rectangle(self.x, self.y,
                self.x + self.size, self.y + self.size,
                fill=color)

    def spawnFood(self):
        x = self.x + random.random()*self.size*self.foodRadius
        x = max(min(WIDTH - 5, x), 0) #boundary check
        y = self.y + random.random()*self.size*self.foodRadius
        y = max(min(HEIGHT - 5, y), 0)

        if random.random() < self.foodChance:
            fate = random.random()
            stackHiMid = self.foodBook["hi"] + self.foodBook["mid"]
            stackAll = stackHiMid  + self.foodBook["lo"]

            if fate < self.foodBook["hi"]:
                Tile.foodList.append(HiFood(x, y))

            elif fate > self.foodBook["hi"] and fate < stackHiMid:
                Tile.foodList.append(MidFood(x, y))

            elif fate > stackHiMid and fate < stackAll:
                Tile.foodList.append(LoFood(x, y))


class Grassland(Tile):
    def __init__(self, x, y, size=TILESIZE):
        super().__init__(x, y, size)
        #for drawing
        self.color = "green"

        #tile food properties
        self.viability = random.random()
        self.threshold = 0.01
        self.isViable = self.viability < self.threshold

        self.foodChance = 1
        self.foodBook = {"hi":0, "mid":0.1, "lo":0.9}
        self.foodRadius = 4

class Forest(Tile):
    pass

class Desert(Tile):
    pass

class Savanna(Tile):
    pass

class Marsh(Tile):
    pass


class Food:
    #basic food class - dont ever use this - subclass
    def __init__(self, x, y, size=10):
        self.x = x #center -BEWARE
        self.y = y
        self.size = size
        self.color = "pink"
        self.id = random.randint(1, 1000000000)

        self.energy = 1

    def draw(self, canvas, color=None):
        if color is None: color = self.color

        canvas.create_oval(self.x - self.size/2, self.y - self.size/2,
                self.x + self.size/2, self.y + self.size/2,
                fill=color, width=0)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Food):
            return self.id == other.id

        else:
            return False

class LoFood(Food):
    def __init__(self, x, y, size=3):
        super().__init__(x, y, size)
        self.color = "limegreen"
        self.energy = 0.2

class MidFood(Food):
    def __init__(self, x, y, size=4):
        super().__init__(x, y, size)
        self.color = "orange"
        self.energy = 1

class HiFood(Food):
    def __init__(self, x, y, size=5):
        super().__init__(x, y, size)
        self.color = "red"
        self.energy = 2

class Corpse(Food):
    def __init__(self, x, y, color, size=10):
        super().__init__(x, y, size)
        self.color = color
        self.energy = 10
