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
        #spawns food around viable tiles
        if random.random() < self.foodChance:
            #figuring out x and y of food randomly
            #spawns in specified radius
            xMult = 1 if random.random() < 0.5 else -1
            x = self.x + random.random()*self.size*self.foodRadius*xMult
            x = max(min(WIDTH - 5, x), 0) #boundary check

            yMult = 1 if random.random() < 0.5 else -1
            y = self.y + random.random()*self.size*self.foodRadius*xMult
            y = max(min(HEIGHT - 5, y), 0)

            fate = random.random()#what type of food?

            #makes the if statements neater
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
        self.threshold = 0.1
        self.isViable = self.viability < self.threshold

        self.foodChance = 0.9
        self.foodBook = {"hi":0, "mid":0.1, "lo":0.9}
        self.foodRadius = 2.5

class Forest(Tile):
    def __init__(self, x, y, size=TILESIZE):
        super().__init__(x, y, size)
        #for drawing
        self.color = "darkgreen"

        #tile food properties
        self.viability = random.random()
        self.threshold = 0.01
        self.isViable = self.viability < self.threshold

        self.foodChance = 1
        self.foodBook = {"hi":0.2, "mid":0.4, "lo":0.4}
        self.foodRadius = 1.5

class Desert(Tile):
    def __init__(self, x, y, size=TILESIZE):
        super().__init__(x, y, size)
        #for drawing
        self.color = "tan"

        #tile food properties
        self.viability = random.random()
        self.threshold = 0.005
        self.isViable = self.viability < self.threshold

        self.foodChance = 0.7
        self.foodBook = {"hi":0.1, "mid":0.0, "lo":0.9}
        self.foodRadius = 3.5

class Savanna(Tile):
    def __init__(self, x, y, size=TILESIZE):
        super().__init__(x, y, size)
        #for drawing
        self.color = "lightbrown"

        #tile food properties
        self.viability = random.random()
        self.threshold = 0.01
        self.isViable = self.viability < self.threshold

        self.foodChance = 0.6
        self.foodBook = {"hi":0, "mid":0.1, "lo":0.9}
        self.foodRadius = 2.5

class Marsh(Tile):
    def __init__(self, x, y, size=TILESIZE):
        super().__init__(x, y, size)
        #for drawing
        self.color = "brown"

        #tile food properties
        self.viability = random.random()
        self.threshold = 0.008
        self.isViable = self.viability < self.threshold

        self.foodChance = 1
        self.foodBook = {"hi":0.3, "mid":0.3, "lo":0.4}
        self.foodRadius = 1.5


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
